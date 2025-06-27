function BlogBlock() {
  return (
    <div className="blog-block">
      <div className="blog-block__inner relative">
        <div className="blog-block__body">
          <img src="" alt="" />
        </div>
        <div className="blog-block__content">
          <div className="blog-block__title md:text-size-h4 text-size-h6 leading-130 text-snow md:mb-4 mb-2 font-bold"></div>
          <div className="blog-block__description font-secondary md:text-size-body-1 text-size-body-5 leading-130"></div>
        </div>
      </div>
    </div>
  );
}

export default BlogBlock;