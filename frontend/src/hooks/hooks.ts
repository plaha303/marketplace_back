import { TypedUseSelectorHook, useSelector as rawUseSelector } from 'react-redux';
import { RootState } from '../store/store';

export const useSelector: TypedUseSelectorHook<RootState> = rawUseSelector;
