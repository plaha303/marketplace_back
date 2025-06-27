import { Button } from '@/UI/Button/Button';
import FacebookIcon from "@/assets/Icons/FacebookIcon.svg?react";
import GoogleIcon from '@/UI/Icons/GoogleIcon';
import PinterestIcon from "@/assets/Icons/PinterestIcon.svg?react";

function PlatformsButtons() {
  return (
    <>
      <div className="platforms flex justify-center gap-4 mb-12">
        <div className="platformsBlock">
          <Button type="button" className="flex items-center platformButton hover:opacity-35 duration-500 w-[56px] h-[56px] p-0 btn-secondary">
            <FacebookIcon className='text-snow'/>
          </Button>
        </div>
        <div className="platformsBlock">
          <Button type="button" className="flex items-center platformButton hover:opacity-35 duration-500 w-[56px] h-[56px] p-0 btn-secondary">
            <PinterestIcon className='text-snow' />
          </Button>
        </div>
        <div className="platformsBlock">
          <Button type="button" className="flex items-center platformButton hover:opacity-35 duration-500 w-[56px] h-[56px] p-0 btn-secondary">
            <GoogleIcon className='text-snow' />
          </Button>
        </div>
      </div>
    </>
  );
}

export default PlatformsButtons;