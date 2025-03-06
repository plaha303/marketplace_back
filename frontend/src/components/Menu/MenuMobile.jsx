import styled from '../Menu/Menu.module.css';
import MenuBottomMobile from "../Menu/MenuBottomMobile"

function MenuMobile({ isButtonClicked,onButtonClick}){
    return(
        <>
            {isButtonClicked && (
                <div
                className="fixed inset-0 bg-black bg-opacity-50 z-0"
                onClick={onButtonClick}
                ></div>
            )}
            <div  className={`absolute w-[45vw] h-[100vh] flex lg:hidden justify-end duration-300 ease-out top-[0] -left-[45vw] bg-[#f1e4ff] ${isButtonClicked? "w-[100vw]" : 'w-[45vw]'} `}>
                <div className={ `flex flex-col  gap-y-[15px] pt-[20px] pr-[30px]`}>
                    <div> Input or Logo ?</div>
                    <div> 
                        <button type="button" className={`flex items-center ${styled.headerBtn__action}`}> 
                            <span className={`icon me-2 ${styled.iconCatalog}`}></span>
                                Каталог
                        </button>
                    </div>
                    <MenuBottomMobile />
                    <div className="flex grow"></div>
                    <div className='flex justify-center items-center h-[8vh] border-t border-black'> SIGN IN?</div>
                </div>
            </div>
        </>
    );
}

export default MenuMobile
