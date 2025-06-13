import { useEffect, useRef } from "react"

export function useClickOutside<T extends HTMLElement>(
  onClickOutside: () => void,
  excludeRefs: React.RefObject<HTMLElement>[] = []
) {
  const ref = useRef<T>(null);

  useEffect(() => {
    function handleClick(event: MouseEvent) {
      const target = event.target as Node;

      const clickedInsideExcluded = excludeRefs.some(
        (excludeRef) => excludeRef.current && excludeRef.current.contains(target)
      );

      if (
        ref.current &&
        !ref.current.contains(target) &&
        !clickedInsideExcluded
      ) {
        onClickOutside();
      }
    }

    document.addEventListener('mousedown', handleClick);
    return () => {
      document.removeEventListener('mousedown', handleClick);
    };
  }, [onClickOutside, excludeRefs]);

  return ref;
}