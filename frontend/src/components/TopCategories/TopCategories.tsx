import { Link } from 'react-router';
import style from './TopCategories.module.scss'

function TopCategories() {
  return (
    <div className={`${style.topCategories} lg:py-[80px] py-12`}>
      <div className="container px-4 mx-auto">
        <div className="top-categories__inner">
          <div className="top-categories__header lg:mb-16 mb-9">
            <h3 className='text-size-h3 uppercase text-accent-800 leading-130'>Популярні категорії</h3>
          </div>

          <div className="top-categories__body flex xl:flex-row flex-col items-start gap-6">
            
            <div className="top-categories__left flex flex-wrap xl:max-w-2/5 xl:flex-2/5 gap-6">

              <div className={`${style.topCategories__block} w-full relative rounded-4xl shadow-custom1 lg:h-[324px] md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full  p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Мистецтво та декор</div>
                </Link>
              </div>

              <div className={`${style.topCategories__block} sm:flex-1  w-full relative rounded-4xl shadow-custom1 md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Одяг та текстиль</div>
                </Link>
              </div>

              <div className={`${style.topCategories__block} sm:max-w-[212px] w-full relative rounded-4xl shadow-custom1 md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Сумки та гаманці</div>
                </Link>
              </div>

            </div>

            <div className="top-categories__right flex-1 flex flex-wrap gap-6">
              <div className={`${style.topCategories__block} sm:max-w-[212px] w-full relative rounded-4xl shadow-custom1 md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Дитячі товари</div>
                </Link>
              </div>
              <div className={`${style.topCategories__block} xl:flex-1 relative sm:flex-1/2 w-full rounded-4xl shadow-custom1 md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Предмети дому</div>
                </Link>
              </div>
              <div className={`${style.topCategories__block} md:max-w-[212px] sm:flex-1 w-full relative rounded-4xl shadow-custom1 md:h-[212px] sm:h-[150px] h-[56px] sm:order-none order-1`}>
                <Link to='/' className={`${style.topCategories__blockInner} ${style.topCategories__blockAllCategories} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Всі категорії</div>
                </Link>
              </div>

              <div className={`${style.topCategories__block}  sm:max-w-[212px] w-full relative rounded-4xl shadow-custom1 lg:h-[324px] md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Аромати та свічки</div>
                </Link>
              </div>
              
              <div className={`${style.topCategories__block} md:flex-1 w-full relative rounded-4xl shadow-custom1 lg:h-[324px] md:h-[212px] sm:h-[150px] h-[56px]`}>
                <Link to='/' className={`${style.topCategories__blockInner} flex items-center justify-center bg-accent-200 rounded-4xl h-full p-4 overflow-hidden font-generale`}>
                  <div className={`${style.topCategories__blockTitle} sm:text-size-h5 text-size-h7 font-bold  text-snow leading-130 relative text-center`}>Прикраси та аксесуари</div>
                </Link>
              </div>

            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default TopCategories;