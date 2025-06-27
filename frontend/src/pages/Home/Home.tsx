import AuctionBlock from "@/components/AuctionBlock/AuctionBlock";
import Features from "@/components/Features/Features";
import HomeBanner from "@/components/HomeBanner/HomeBanner";
import SliderWithProducts from "@/components/SliderWithProducts/SliderWithProducts";
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
		</div>
	);
}

export default Home;