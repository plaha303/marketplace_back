import AppRoute from "@/routers/enums/routers-enums";

export type FooterLinks = {
  id: number;
  label?: string;
  path: string;
}

export const footerLinks1: FooterLinks[]  = [
  {id: 1, label: 'Каталог', path: AppRoute.ROOT},
  {id: 2, label: 'Майстри', path: AppRoute.ROOT},
  {id: 3, label: 'Live Аукціон', path: AppRoute.ROOT},
  {id: 4, label: 'Хіти продаж', path: AppRoute.ROOT},
  {id: 5, label: 'Спеціальні пропозиції', path: AppRoute.ROOT},
  {id: 6, label: 'Майстер-класи', path: AppRoute.ROOT},
]

export const footerLinks2: FooterLinks[] = [
  { id: 1, label: 'Про платформу', path: AppRoute.ABOUT },
  { id: 2, label: 'Контакти', path: AppRoute.CONTACT },
  { id: 3, label: 'Допомога', path: AppRoute.SUPPORT },
  { id: 4, label: 'Програма лояльності', path: AppRoute.REGISTRATION },
  { id: 5, label: 'Блог', path: AppRoute.BLOG },
]

export const footerLinks3: FooterLinks[] = [
  { id: 1, label: 'Реєстрація', path: AppRoute.REGISTRATION },
  { id: 2, label: 'Оплата і доставка', path: AppRoute.CONTACT },
  { id: 3, label: 'Умови повернення', path: AppRoute.SUPPORT },
  { id: 4, label: 'Кошик', path: AppRoute.BASKET },
  { id: 5, label: 'Обране', path: AppRoute.FAVORITE },
]

export const footerBottomLinks: FooterLinks[] = [
  { id: 1, label: 'Політика конфіденційності', path: AppRoute.PRIVACY_POLICY },
  { id: 2, label: 'Згода на обробку персональних даних', path: AppRoute.PROCESSING_PERSONAL_DATA },
  { id: 3, label: 'Умови надання послуг', path: AppRoute.TERMS_SERVICE },
]