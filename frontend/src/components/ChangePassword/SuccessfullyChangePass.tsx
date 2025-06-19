import AuthLayout from "@/layout/AuthLayout/AuthLayout";
import AppRoute from "@/routers/enums/routers-enums";
import { Button } from "@/UI/Button/Button";
import SuccessfullyChangePassIcon from "@/UI/Icons/SuccessfullyChangePassIcon";
import { Link } from "react-router";

function SuccessfullyChangePass() {
  return (
    <AuthLayout>
      <div>
        <div className="successfully__header">
          <div className="mb-12">
            <div className="mb-8">
              <SuccessfullyChangePassIcon className="text-accent-600" />
            </div>
            <h2 className="auth__title text-size-h2 mb-6 leading-100 text-accent-800 font-bold">Успішно</h2>
            <div className="text-primary-600 leading-130 text-size-h6 mb-6">Ваш пароль змінено</div>
            <div className="max-w-[500px] mx-auto">
              <p>Потрібна допомога?</p>
              <p>Якщо у вас виникли питання або потрібна допомога, не соромтеся зв'язатися з нами. Ми завжди раді допомогти!</p>
              <p>Дякуємо, що приєдналися до нас. </p>
              <p>Насолоджуйтесь своїм часом на нашому сайті!</p>
            </div>
          </div>
          <div className="flex gap-6">
            <div className="flex-1/2">
              <Button asChild className="btn-primary h-[55px] font-secondary text-size-body-2 font-bold leading-100">
                <Link to={AppRoute.LOGIN}>Вхід</Link>
              </Button>
            </div>
            <div className="flex-1/2">
              <Button asChild className="btn-secondary h-[55px] font-secondary text-size-body-2 font-bold leading-100">
                <Link to={AppRoute.ROOT}>Головна</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </AuthLayout>
  );
}

export default SuccessfullyChangePass;