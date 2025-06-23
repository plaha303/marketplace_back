export function isDefined<T>(value: T | null | undefined): value is NonNullable<T> {
  return value !== undefined && value !== null
} 

export function isBlob(value: any): value is Blob {
  return (
    typeof value === 'object' &&
    typeof value.type === 'string' &&
    typeof value.stream === 'function' &&
    typeof value.arrayBuffer === 'function' &&
    typeof value.constructor === 'function' &&
    typeof value.constructor.name === 'string' &&
    /^(Blob|File)$/.test(value.constructor.name) &&
    /^(Blob|File)$/.test(value[Symbol.toStringTag])
  );
}


export function isString(value: any): value is string {
  return typeof value === 'string'
}

export function isFormData(value: any): value is FormData {
  return value instanceof FormData;
}

export function isSuccess(status: number): boolean {
  return status >= 200 && status < 300 
}

export function shallowStringify(obj: Record<string, unknown>, maxArrayLength = 5) {
  const replacer = (_key: string, value: unknown) => {
    if (Array.isArray(value) && value.length > maxArrayLength) {
      return [
        ...value.slice(0, maxArrayLength),
        `...more (${value.length - maxArrayLength}) items`,
      ];
    }
    return value;
  };

  return JSON.stringify(obj, replacer, '\t');
};


export function formatTimeForAuction(isoString: string): { hours: string, minutes: string, seconds: string } {
  const date = new Date(isoString);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');

  return { hours, minutes, seconds };
}