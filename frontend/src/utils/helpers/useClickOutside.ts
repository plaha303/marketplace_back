import { useCallback, useEffect, useMemo, useRef } from 'react';

interface Props {
  onTriggered: (e: Event) => void;
  disableClick?: boolean;
  disableTouch?: boolean;
  disableKeys?: boolean;
  allowAnyKey?: boolean;
  triggerKeys?: string[];
  excludeRefs?: React.RefObject<HTMLElement | null>[]
}

type EventConfigItem = [boolean | undefined, string, (e: Event) => void];

/**
 * Хук для детектирования клика вне компонента (и/или нажатия клавиш).
 * Работает корректно с порталами и shadow DOM.
 */
export function useClickOutside({
  onTriggered,
  disableClick,
  disableTouch,
  disableKeys,
  allowAnyKey,
  triggerKeys,
  excludeRefs = [],
}: Props) {
  const ref = useRef<HTMLElement | null>(null);

  const keyListener = useCallback(
    (e: KeyboardEvent) => {
      if (allowAnyKey) {
        onTriggered(e);
      } else if (triggerKeys) {
        if (triggerKeys.includes(e.key)) {
          onTriggered(e);
        }
      } else {
        if (e.key === 'Escape') {
          onTriggered(e);
        }
      }
    },
    [allowAnyKey, triggerKeys, onTriggered]
  );

  const clickOrTouchListener = useCallback(
    (e: MouseEvent | TouchEvent) => {
      if (!ref.current) return;

      const eventPath = e.composedPath ? e.composedPath() : [];

      // Если клик внутри основного элемента — не закрывать
      if (eventPath.includes(ref.current)) return;

      // Если клик внутри исключаемых элементов — не закрывать
      if (excludeRefs.some(r => r.current && eventPath.includes(r.current))) return;

      onTriggered?.(e);
    },
    [excludeRefs, onTriggered]
  );

  const eventsConfig: EventConfigItem[] = useMemo(
    () => [
      [disableClick, 'click', clickOrTouchListener],
      [disableTouch, 'touchstart', clickOrTouchListener],
      [disableKeys, 'keyup', keyListener],
    ],
    [disableClick, disableTouch, disableKeys, clickOrTouchListener, keyListener]
  );

  useEffect(() => {
    eventsConfig.forEach(([isDisabled, eventName, listener]) => {
      if (!isDisabled) {
        document.addEventListener(eventName, listener);
      }
    });

    return () => {
      eventsConfig.forEach(([isDisabled, eventName, listener]) => {
        if (!isDisabled) {
          document.removeEventListener(eventName, listener);
        }
      });
    };
  }, [eventsConfig]);

  return ref;
}
