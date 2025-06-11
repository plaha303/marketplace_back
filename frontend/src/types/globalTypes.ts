const Languages = {
  UA: 'UA',
  US: 'US'
} as const;

const Currency = {
  UAH: 'UAH',
  USD: 'USD'
} as const;

type Languages = (typeof Languages)[keyof typeof Languages];
type Currency = (typeof Currency)[keyof typeof Currency];

export {Languages, Currency}