import SearchIcon from '@/UI/Icons/SearchIcon';
import BaseInput from '@/UI/Input/BaseInput';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router';


function SearchBlock() {
  const {handleSubmit, register, formState: { errors }} = useForm();
  const navigate = useNavigate();
  function onSubmit(data: {data: string}) {
    console.log('data search', data)
  }

  return (
    <div className='search-block'>
      <form className="search-block__input relative" onSubmit={handleSubmit(onSubmit)}>
        <span className='search-block__icon absolute top-1/2 -translate-y-1/2 left-4'>
          <SearchIcon className='text-primary-400' />
        </span>
        <BaseInput 
          {...register('search', { required: true })} 
          hasError={!!errors.search}
          placeholder='Шукати товар, майстра,  бренд' 
          className='p-4 pl-12 h-[56px] bg-snow focus-visible:ring-0 placeholder:text-primary-400 text-primary-900' 
        />
      </form>
    </div>
  );
}

export default SearchBlock;