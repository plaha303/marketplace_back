import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation } from 'swiper/modules';
import {Link} from "react-router"
import "swiper/css";
import "swiper/css/bundle"
// import 'swiper/css/navigation';
// import 'swiper/css/pagination';

function HomeSlider() {
  const slider = [
    {
      id: '1',
      title: 'Унікальні ручні вироби',
      description: 'Відкрийте для себе нашу колекцію унікальних ручних виробів, створених талановитими майстрами.',
      img: 'slide-1.png',
      link: 'LogIn',
      btnText: 'Приєднатись до спільноти'
    },
    {
      id: '2',
      title: 'Шукайте та продавайте товари онлайн',
      description: 'Долучіться до спільноти людей, які цінують ручну роботу та зберігають традиції майстерності',
      img: 'slide-2.png',
      link: '#',
      btnText: 'Приєднатись до спільноти'
    },
    {
      id: '3',
      title: 'Ексклюзивні крафтові товари',
      description: 'Знайдіть ексклюзивні крафтові товари, створені із застосуванням традиційних технік і сучасного дизайну.',
      img: 'slide-3.png',
      link: '#',
      btnText: 'Приєднатись до спільноти'
    },
  ]
  return (
    <div className='home-banner bg-[#e5caff]'>
      <div className="container mx-auto">
        <Swiper
          modules={[Navigation]}
          spaceBetween={0}
          slidesPerView={1}
          loop={true}
          navigation
        >
          {slider.map(slide => (
            <SwiperSlide key={slide.id}>
              <div className="slider-block">
                <div className="flex gap-x-[20px] items-center">
                  <div className="slider-block__left basis-1/2">
                    <h2 className="text-5xl font-bold">{slide.title}</h2>
                    <p className="py-6">{slide.description}</p>
                    <div className='max-w-[415px]'>
                      <Link to={slider.link} className="w-full block px-6 py-3 rounded-lg text-white font-semibold text-2xl text-center baseBtn__blue">{slide.btnText}</Link>
                    </div>
                  </div>
                  <div className="slider-block__right basis-1/2">
                    <img
                      src={`/img/home-slider/${slide.img}`}
                      className="max-w-full w-full rounded-[24px]" />
                  </div>
                </div>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </div>
  );
}

export default HomeSlider;