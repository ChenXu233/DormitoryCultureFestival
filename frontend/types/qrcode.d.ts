declare module 'qrcode' {
  export function toDataURL(data: string, options?: any): Promise<string>
  export function toDataURL(data: string, options: any, cb: (err: any, url?: string) => void): void
  export function toCanvas(canvas: HTMLCanvasElement, text: string, options?: any): Promise<void>
  export function toCanvas(canvas: HTMLCanvasElement, text: string, options: any, cb: (err: any) => void): void
  export function toFile(path: string, text: string, options?: any): Promise<void>
}
