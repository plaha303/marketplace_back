import { featuresType } from "./types";

function Features() {
  return (
    <div className="features bg-primary-900 lg:py-[80px] py-12">
      <div className="container px-4 m-auto">
        <div className="features__header max-w-[800px] mx-auto lg:mb-16 mb-9">
          <div className="features__header-title uppercase text-size-h3 lg:mb-10 mb-4 leading-130 text-center text-snow">Про платформу</div>
          <div className="features__header-subtitle text-size-body-1  lg:text-center text-snow leading-130">
            ArtLance – простір автентичних продуктів,<br/> де майстри та цінителі хендмейду зустрічаються,<br/>  щоб створювати, продавати та знаходити унікальні речі. 
          </div>
        </div>
        <div className="features__body">
          <div className="features__blocks flex justify-between lg:flex-row flex-col xl:px-15 xl:gap-0 gap-4">
            {featuresType.map(feature => {
              const Icon = feature.icon;
              return ( 
                <div className="features__block lg:max-w-[330px]" key={feature.id}>
                  <div className="features__block-top lg:mb-6 mb-2">
                    <Icon />
                  </div>
                  <div className="features__block-body">
                    <div className="features__block-title text-size-h5 lg:mb-4 mb-2 text-snow leading-130">{feature.title}</div>
                    <div className="features__block-text lg:text-size-body-2 text-size-body-3 text-snow leading-130 font-secondary">{feature.text}</div>
                  </div>
                </div>)
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Features;