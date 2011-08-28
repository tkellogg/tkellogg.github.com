describe("BlogLoader", function() {
	
	describe("when loading blog posts", function() {
		var sut = undefined;
		var load = sinon.spy();

		beforeEach(function() {
			sut = new BlogLoader("test-url");
			sut.bind("load", load);
		});

		it("invokes the 'load' event when the first posts load", sinon.test(function() {
			this.mock($).expects("ajax").once();
			sut.sync();
			
			expect(load.wasCalled).toBeTruthy();
		}));

	});

});
