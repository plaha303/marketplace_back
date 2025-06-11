import { FieldValues, Path, UseFormRegister } from "react-hook-form";

export interface BaseInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  hasError?: boolean,
  className?: string
}

export interface InputProps<T extends FieldValues> {
  name: Path<T>;
  type: string;
  register?: UseFormRegister<T>;
  className?: string,
  label?: string;
  required?: boolean;
  hasError?: boolean;
  validationText?: string;
}
export interface PasswordToggleProps {
  onToggle: () => void;
  isVisible: boolean;
}