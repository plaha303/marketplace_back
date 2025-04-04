import ImageSlider from '../../UI/Slider/ImageSlider';

const sliders = [
  {
    id: 1,
    title: 'Унікальні ручні вироби',
    description: 'Відкрийте для себе нашу колекцію унікальних ручних виробів, створених талановитими майстрами. ',
    imgSrc: '/homeSlide1.png',
    textBtn: 'Приєднатись до спільноти',
    link: '#'
  },
  {
    id: 2,
    title: 'Шукайте та продавайте товари онлайн',
    description: 'Долучіться до спільноти людей, які цінують ручну роботу та зберігають традиції майстерності ',
    imgSrc: '/homeSlide2.png',
    textBtn: 'Приєднатись до спільноти',
    link: '#'
  },
  {
    id: 3,
    title: 'Ексклюзивні крафтові товари',
    description: 'Знайдіть ексклюзивні крафтові товари, створені із застосуванням традиційних технік і сучасного дизайну.',
    imgSrc: '/homeSlide3.png',
    textBtn: 'Приєднатись до спільноти',
    link: '#'
  },
]

function HomeBanner() {
  return (
    <>
      <ImageSlider sliders={sliders} dots={false} arrows={true} slidesToShow={1} slidesToScroll={1} />
    </>
  );
}

export default HomeBanner;