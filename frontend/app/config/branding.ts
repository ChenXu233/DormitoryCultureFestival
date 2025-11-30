export interface BrandingConfig {
  collegeName: string
  logoPath: string // public path (to be provided later)
  slogan?: string
  eventName?: string
}

export const branding: BrandingConfig = {
  collegeName: '信息科学与工程学院',
  logoPath: '/logo.jpg', // TODO: replace when real logo provided
  slogan:'Powered by CIC计算机信息交流协会',
  eventName: 'Dormitory Culture Festival'
}
