import SearchIcon from '@/UI/Icons/SearchIcon';
import BaseInput from '@/UI/Input/BaseInput';


function SearchBlock() {
  return (
    <div className='search-block'>
      <div className="search-block__input relative">
        <span className='search-block__icon absolute top-1/2 -translate-y-1/2 left-4'>
          <SearchIcon className='text-primary-400' />
        </span>
        <BaseInput placeholder='Шукати товар, майстра,  бренд' className='p-4 pl-12 h-[56px] bg-snow focus-visible:ring-0 placeholder:text-primary-400 text-primary-900' />
      </div>
    </div>
  );
}

export default SearchBlock;