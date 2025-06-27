import AuctionBlock from "@/components/AuctionBlock/AuctionBlock";
import Features from "@/components/Features/Features";
import HomeBanner from "@/components/HomeBanner/HomeBanner";
import SliderWithBlog from "@/components/SliderWithBlog/SliderWithBlog";
import SliderWithProducts from "@/components/SliderWithProducts/SliderWithProducts";
import SliderWithReviews from "@/components/SliderWithReviews/SliderWithReviews";
import SpecialOffers from "@/components/SpecialOffers/SpecialOffers";
import Subscription from "@/components/Subscription/Subscription";
import TopCategories from "@/components/TopCategories/TopCategories";

function Home() {
	return (
		<div className="home-page">
      <HomeBanner />
			<Features />
			<AuctionBlock />
			<TopCategories />
			<SliderWithProducts title="Хіти продаж" watchAll='/' />
			<SpecialOffers />
			<SliderWithProducts title="Товари зі знижками" watchAll='/' />
			<Subscription />
			<SliderWithReviews title="Відгуки" watchAll='/' />
			<SliderWithBlog title="Блог" watchAll='/' />
		</div>
	);
}

export default Home;