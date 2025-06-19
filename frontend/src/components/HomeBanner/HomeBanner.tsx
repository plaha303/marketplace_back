import BaseSlider from "@/UI/Slider/BaseSlider";

function HomeBanner() {
  return (
    <div className="home-banner pattern-bg">
      <div className="container px-4 mx-auto">
        <BaseSlider pagination={true}>
          <div className="home-banner__slide">

          </div>
        </BaseSlider>
      </div>
    </div>
  );
}

export default HomeBanner;