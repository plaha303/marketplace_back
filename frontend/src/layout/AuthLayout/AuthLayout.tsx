import { ReactNode } from "react";

function AuthLayout({children, title, subtitle}: {children: ReactNode, title?: string, subtitle?: string}) {
  return (
    <div className="pattern-bg lg:py-[80px] py-[40px]">
      <div className="container mx-auto px-4">
        <div className="max-w-[685px] mx-auto bg-snow-70 shadow-custom1 lg:p-12 px-6 py-10 rounded-5xl">
          <div className="auth__header lg:mb-12 mb-6">
            <h2 className="auth__title text-size-h2 mb-2 leading-100 text-accent-800">{title}</h2>
            <div className="auth__subtitle text-size-body-1 leading-130">
              {subtitle}
            </div>
          </div>

          {children}
        </div>
      </div>
    </div>
  );
}

export default AuthLayout;