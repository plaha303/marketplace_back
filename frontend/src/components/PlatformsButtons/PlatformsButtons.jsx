import React from 'react';

function PlatformsButtons() {
  return (
    <>
      <div className="platforms flex justify-between mb-[24px]">
        <div className="platformsBlock">
          <button type="button" className="flex items-center platformButton hover:opacity-35 duration-500">
            <img src="/img/icons/google.svg" alt="Google" className="me-2" />
            <span className="font-semibold">Google</span>
          </button>
        </div>
        <div className="platformsBlock">
          <button type="button" className="flex items-center platformButton hover:opacity-35 duration-500">
            <img src="/img/icons/facebook.svg" alt="facebook" className="me-2" />
            <span className="font-semibold">Facebook</span>
          </button>
        </div>
        <div className="platformsBlock">
          <button type="button" className="flex items-center platformButton hover:opacity-35 duration-500">
            <img src="/img/icons/apple.svg" alt="facebook" className="me-2" />
            <span className="font-semibold">Apple</span>
          </button>
        </div>
      </div>

      <div>
        <p>
          <a href='#' className='underline hover:text-blue-600 duration-500'>Створюючи обліковий запис</a>, ви приймаєте наші <a href='#' className="underline hover:text-blue-600 duration-500">Умови надання послуг та Політику конфіденційності</a>.
        </p>
      </div>
    </>
  );
}

export default PlatformsButtons;