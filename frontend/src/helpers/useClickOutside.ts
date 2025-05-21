import { useEffect, useRef } from "react"

export function useClickOutside<T extends HTMLElement>(onClickOutSide: () => void) {
  const ref = useRef<T>(null);

  useEffect(() => {
    function handleClick(event: MouseEvent) {
      if(ref.current && !ref.current.contains(event?.target as Node)) {
        onClickOutSide();
      }
    }

    document.addEventListener('mousedown', handleClick);

    return () => {
      document.removeEventListener('mousedown', handleClick)
    }
  }, [onClickOutSide])

  return ref;
}