export {}

declare global {
  interface Window {
    electronAPI?: {
      send: (channel: string, payload?: any) => void
      receive: (channel: string, func: (...args: any[]) => void) => void
    }
  }
}
