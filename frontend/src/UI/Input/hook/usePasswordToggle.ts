import { useCallback, useState } from "react";

function usePasswordToggle() {
  const [passwordShow, setPasswordShow] = useState(false);

  const togglePassword = useCallback(() => {
    setPasswordShow(prev => !prev);
  }, [])

  return {passwordShow, togglePassword}
}

export default usePasswordToggle;