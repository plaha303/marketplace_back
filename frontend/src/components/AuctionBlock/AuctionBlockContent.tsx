import { Button } from '@/UI/Button/Button';


function AuctionBlockContent() {
  return (
    <div className="auction-block__content lg:p-12 md:p-6 p-4 rounded-4xl shadow-custom2 bg-snow-70">
      <div className="auction-block__content-top lg:mb-14 mb-8">
        <div className="auction-block__content-title uppercase text-size-h3 lg:mb-10 mb-4 leading-130 text-accent-800">
          Відчуй азарт реального аукціону!
        </div>
        <div className="auction-block__content-text font-secondary md:text-size-body-1 text-size-body-3 leading-130 ">
          Тут ви можете змагатися за ексклюзивні вироби, 
          підтримувати талановитих майстрів та отримувати унікальні речі,  
          які створені спеціально для унікальних цінителів.
        </div>
      </div>
      <div className="auction-block__content-actions flex md:gap-4 gap-2">
        <Button variant="default" className="font-bold md:text-size-body-2 text-size-body-3 md:px-10.5 md:py-4 p-4 font-secondary">Календар</Button>
        <Button variant="secondary" className="font-bold md:text-size-body-2 text-size-body-3 md:px-10.5 md:py-4 p-4 font-secondary">Про аукціон</Button>
      </div>
    </div>
  );
}

export default AuctionBlockContent;