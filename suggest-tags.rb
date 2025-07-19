#!/usr/bin/env ruby

require 'yaml'
require 'date'

# Configuration
POSTS_DIR = '_posts'
RECENCY_WEIGHT = 0.4  # Weight for recency (0-1)
FREQUENCY_WEIGHT = 0.6  # Weight for frequency (0-1)
HALF_LIFE_DAYS = 180  # Days for recency decay

def extract_frontmatter(file_path)
  content = File.read(file_path)
  if content =~ /\A---\s*\n(.*?)\n---\s*\n/m
    begin
      YAML.safe_load($1, permitted_classes: [Date, Time])
    rescue => e
      puts "Warning: Failed to parse YAML in #{file_path}: #{e.message}"
      nil
    end
  else
    nil
  end
end

def get_post_date(file_path, frontmatter)
  # Try to get date from frontmatter first
  if frontmatter && frontmatter['date']
    begin
      return Date.parse(frontmatter['date'].to_s)
    rescue
      # Fall through to filename parsing
    end
  end
  
  # Extract date from filename (YYYY-MM-DD format)
  if File.basename(file_path) =~ /^(\d{4})-(\d{2})-(\d{2})-/
    Date.new($1.to_i, $2.to_i, $3.to_i)
  else
    nil
  end
end

def calculate_recency_score(date, today)
  return 0 unless date
  
  days_ago = (today - date).to_i
  # Exponential decay with half-life
  Math.exp(-0.693 * days_ago / HALF_LIFE_DAYS)
end

def analyze_categories
  today = Date.today
  category_data = Hash.new { |h, k| h[k] = { count: 0, dates: [], posts: [] } }
  
  # Process all posts
  Dir.glob(File.join(POSTS_DIR, '*.md')).each do |file_path|
    frontmatter = extract_frontmatter(file_path)
    next unless frontmatter
    
    categories = frontmatter['categories'] || []
    categories = [categories] unless categories.is_a?(Array)
    
    date = get_post_date(file_path, frontmatter)
    
    categories.each do |category|
      next if category.nil? || category.to_s.strip.empty?
      
      category_str = category.to_s.strip
      category_data[category_str][:count] += 1
      category_data[category_str][:dates] << date if date
      category_data[category_str][:posts] << File.basename(file_path)
    end
  end
  
  # Calculate weighted scores
  scored_categories = category_data.map do |category, data|
    # Frequency score (normalized)
    max_count = category_data.values.map { |d| d[:count] }.max.to_f
    frequency_score = data[:count] / max_count
    
    # Recency score (average of all post recencies for this category)
    recency_scores = data[:dates].map { |date| calculate_recency_score(date, today) }
    avg_recency_score = recency_scores.empty? ? 0 : recency_scores.sum / recency_scores.length
    
    # Combined weighted score
    total_score = (FREQUENCY_WEIGHT * frequency_score) + (RECENCY_WEIGHT * avg_recency_score)
    
    {
      category: category,
      count: data[:count],
      latest_date: data[:dates].max,
      frequency_score: frequency_score,
      recency_score: avg_recency_score,
      total_score: total_score,
      posts: data[:posts].sort.last(3)  # Show last 3 posts
    }
  end
  
  # Sort by total score (descending)
  scored_categories.sort_by { |c| -c[:total_score] }
end

# Main execution
puts "Analyzing blog post categories..."
puts "=" * 60
puts

categories = analyze_categories

if categories.empty?
  puts "No categories found in posts."
  exit
end

# Display results
puts "Top Categories (sorted by weighted score):"
puts "-" * 60
puts "Weights: Frequency=#{FREQUENCY_WEIGHT}, Recency=#{RECENCY_WEIGHT}, Half-life=#{HALF_LIFE_DAYS} days"
puts

categories.each_with_index do |cat, idx|
  puts "#{idx + 1}. #{cat[:category]}"
  #puts "   Count: #{cat[:count]} posts"
  #puts "   Latest: #{cat[:latest_date] || 'N/A'}"
  #puts "   Scores: frequency=#{cat[:frequency_score].round(3)}, recency=#{cat[:recency_score].round(3)}, total=#{cat[:total_score].round(3)}"
  #puts "   Recent posts: #{cat[:posts].join(', ')}"
  #puts
end

# Quick reference list
puts "\nQuick copy-paste list:"
puts "-" * 60
puts categories.take(10).map { |c| " - #{c[:category]}" }.join("\n")
