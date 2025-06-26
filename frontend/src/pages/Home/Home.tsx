import AuctionBlock from "@/components/AuctionBlock/AuctionBlock";
import Features from "@/components/Features/Features";
import HomeBanner from "@/components/HomeBanner/HomeBanner";
import TopCategories from "@/components/TopCategories/TopCategories";

function Home() {
	return (
		<div className="home-page">
      <HomeBanner />
			<Features />
			<AuctionBlock />
			<TopCategories />
		</div>
	);
}

export default Home;