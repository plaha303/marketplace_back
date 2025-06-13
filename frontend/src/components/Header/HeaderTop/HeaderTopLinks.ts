import AppRoute from "@/routers/enums/routers-enums";

export type headerTopLinksProps = {
  id: number;
  label?: string;
  path: string;
}

export const headerTopLinks:headerTopLinksProps[] = [
  { id: 1, label: 'Про платформу', path: AppRoute.ABOUT },
  { id: 2, label: 'Контакти', path: AppRoute.CONTACT },
  { id: 3, label: 'Допомога', path: AppRoute.SUPPORT },
  { id: 4, label: 'Реєстрація', path: AppRoute.REGISTRATION },
]