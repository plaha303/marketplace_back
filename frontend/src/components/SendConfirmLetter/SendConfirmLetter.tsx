import AuthLayout from "@/layout/AuthLayout/AuthLayout";
import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import SuccessfullyChangePassIcon from "@/assets/Icons/SuccessfullyChangePassIcon.svg?react";
import { Link, useLocation, useNavigate } from "react-router";
import { useEffect } from "react";

function SendConfirmLetter() {
  const location = useLocation();
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!location.state?.fromSignUp) {
      navigate('/');
    }
  }, [location, navigate]);

  return (
    <AuthLayout>
      <div>
        <div className="successfully__header">
          <div className="mb-12">
            <div className="mb-8 flex justify-center">
              <SuccessfullyChangePassIcon />
            </div>
            <h2 className="auth__title text-size-h2 mb-6 leading-100 text-accent-800 font-bold text-center">Успішно</h2>
            <div className="text-primary-900 leading-130 text-size-h6 mb-6 text-center max-w-[400px] mx-auto">Перевірте свій e-mail для підтвердження реєстрації</div>
            <div className="max-w-[500px] mx-auto text-center">
              <p className="leading-130 font-secondary text-size-body-3">Потрібна допомога?</p>
              <p className="leading-130 font-secondary text-size-body-3">Якщо у вас виникли питання або потрібна допомога, не соромтеся зв'язатися з нами. Ми завжди раді допомогти!</p>
              <p className="leading-130 font-secondary text-size-body-3">Дякуємо, що приєдналися до нас. </p>
              <p className="leading-130 font-secondary text-size-body-3">Насолоджуйтесь своїм часом на нашому сайті!</p>
            </div>
          </div>
          <div className="flex gap-6">
            <div className="flex-1/2">
              <Button asChild variant="default" className="btn-primary h-[55px] font-secondary text-size-body-2 font-bold leading-100 w-full">
                <Link to={AppRoute.LOGIN}>Вхід</Link>
              </Button>
            </div>
            <div className="flex-1/2">
              <Button asChild variant="secondary" className="btn-secondary h-[55px] font-secondary text-size-body-2 font-bold leading-100 w-full">
                <Link to={AppRoute.ROOT}>Головна</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </AuthLayout>
  );
}

export default SendConfirmLetter;