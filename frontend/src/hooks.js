import { useState } from 'react'

export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    const value = window.localStorage.getItem(key)
    if (value !== undefined) {
      return value
    }
    return initialValue
  })

  const setValue = (value) => {
    window.localStorage.setItem(key, value)
    setStoredValue(value)
  }

  return [storedValue, setValue]
}
