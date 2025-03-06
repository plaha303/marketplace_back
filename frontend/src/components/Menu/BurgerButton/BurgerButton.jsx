function BurgerButton ({onButtonClick}) {

    return (
        <div onClick={onButtonClick} className={`btn flex lg:hidden justify-center items-center min-w-[24px] min-h-[24px] px-[12px] ml-[12px]`}>
            <div class="indicator">
                <span class="indicator-item badge badge-secondary">1</span>
                <svg
                    class="fill-current"
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    viewBox="0 0 512 512">
                    <path d="M64,384H448V341.33H64Zm0-106.67H448V234.67H64ZM64,128v42.67H448V128Z" />
                </svg>
            </div>
        </div>
    )
}

export default BurgerButton;