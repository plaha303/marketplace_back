import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/UI/Select/select";
import { RegionalCurrency, RegionalLanguages } from "./types/RegionalSettingsValues";
import { useState } from "react";
import { Currency, Languages } from "@/types/globalTypes";

import styled from './RegionalSettings.module.scss'
import classNames from "classnames";

function RegionalSettings() {
  const [selectedLanguages, setSelectedLanguages] = useState<Languages>(Languages.UA);
  const [selectedCurrency, setSelectedCurrency] = useState<Currency>(Currency.UAH)

  return (
    <div className='regional-settings'>
      <div className='flex items-center'>
        <div className={classNames('relative', styled.languagesBlock)}>
          <Select value={selectedLanguages} onValueChange={(value: Languages) => setSelectedLanguages(value)}>
            <SelectTrigger className="border-0 regional_btn opacity-100 focus-visible:ring-0 py-2 px-4 min-w-[84px] min-h-[40px] hover:text-accent-600 duration-500" 
              iconClassName="w-[20px] h-[20px]"
            >
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="min-w-[50px]">
              {RegionalLanguages.map(lang => (
                <SelectItem value={lang.label} key={lang.id}>{lang.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className={classNames('relative', styled.currencyBlock)}>
          <Select value={selectedCurrency} onValueChange={(value: Currency) => setSelectedCurrency(value)}>
            <SelectTrigger className="border-0 regional_btn opacity-100 focus-visible:ring-0  py-2 px-4 min-w-[96px] min-h-[40px] hover:text-accent-600 duration-500" 
              iconClassName="w-[20px] h-[20px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="min-w-[50px]">
              {RegionalCurrency.map(currency => (
                <SelectItem value={currency.label} key={currency.id}>{currency.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}

export default RegionalSettings;