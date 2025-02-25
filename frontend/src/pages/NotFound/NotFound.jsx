import { Link } from 'react-router';

const NotFound = () => {
    return (
      <div className='container flex flex-col justify-around items-center pb-[86px]'>
        <div className="flex">
            <img src="/img/404.svg" alt="OOPS! Помилка. Сторінка не знайдена!"/>
        </div>
        <div className='mb-[36px] text-[#31426D] capitalize lg:text-[32px] md:text-[24px] ms:text-[18px] text-[14px] font-semibold leanding-[34px]
            font-(family-name:"Fira Sans Condensed")'>
            OOPS! Помилка. Сторінка не знайдена!
        </div>
        <Link to="/">
            <div className='btn btn-primary flex justify-center items-center 
                text-[#FBFCF3] lg:text-[24px] md:text-[18px] ms:text-[14px] text-[10-px] 
                leanding-[36px] font-semibold bg-blue-600 
                lg:px-[36px] md:px-[24px] sm:px-[16px] px-[12px] py-[16px] 
                rounded-[8px]
                '>
                Повернутися на головну сторінку
            </div>
        </Link>
      </div>
    );
  };
  
  export default NotFound;

