import AuctionBlock from "@/components/AuctionBlock/AuctionBlock";
import Features from "@/components/Features/Features";
import HomeBanner from "@/components/HomeBanner/HomeBanner";

function Home() {
	return (
		<div className="home-page">
      <HomeBanner />
			<Features />
			<AuctionBlock />
		</div>
	);
}

export default Home;