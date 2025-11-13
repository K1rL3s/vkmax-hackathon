export interface UserData {
  id: number
  first_name?: string
  last_name?: string
  username?: string
  language_code?: string
  photo_url?: string
}

export interface ChatData {
  id: number
  type: string
}

export interface InitData {
  hash?: string
  ip?: string
  query_id?: string
  start_param?: string
  auth_date?: number
  user?: UserData
  chat?: ChatData
}

export interface StorageHandler {
  saveKey: (params: { key: string; value: string | null }) => Promise<any>
  getKey: (params: { key: string }) => Promise<any>
  clearKeys: () => Promise<any>
}

export declare class DeviceStorage {
  setItem(key: string, value: string): Promise<any>
  getItem(key: string): Promise<any>
  removeItem(key: string): Promise<any>
  clear(): Promise<any>
}

export declare class SecureStorage extends DeviceStorage {}

export declare class BackButton {
  readonly isVisible: boolean
  show(): void
  hide(): void
}

export interface BiometryInfo {
  available: boolean
  accessRequested: boolean
  accessGranted: boolean
  type: Array<string>
  tokenSaved: boolean
  deviceId: string | null
}

export declare class BiometricManager {
  readonly isInited: boolean
  readonly isBiometricAvailable: boolean
  readonly isAccessRequested: boolean
  readonly isAccessGranted: boolean
  readonly isBiometricTokenSaved: boolean
  readonly biometricType: Array<string>
  readonly deviceId: string | null

  init(): Promise<BiometryInfo>
  requestAccess(reason: string): Promise<BiometryInfo>
  authenticate(reason: string): Promise<any>
  updateBiometricToken(token: string, reason?: string): Promise<any>
  openSettings(): Promise<any>
}

export type ImpactStyle = 'light' | 'medium' | 'heavy' | 'rigid' | 'soft'
export type NotificationType = 'success' | 'warning' | 'error'

export declare class HapticFeedback {
  impactOccurred(
    style: ImpactStyle,
    disableVibrationFallback?: boolean,
  ): Promise<any>
  notificationOccurred(
    type: NotificationType,
    disableVibrationFallback?: boolean,
  ): Promise<any>
  selectionChanged(disableVibrationFallback?: boolean): Promise<any>
}

export declare class ScreenCapture {
  readonly isScreenCaptureEnabled: boolean
  enableScreenCapture(): Promise<any>
  disableScreenCapture(): Promise<any>
}

export declare class SwipesBehavior {
  readonly isEnabled: boolean
  enable(): Promise<any>
  disable(): Promise<any>
}

export interface WebApp {
  readonly initData: string | null
  readonly initDataUnsafe: InitData
  readonly platform: string | null
  readonly version: string | null

  readonly DeviceStorage: DeviceStorage
  readonly SecureStorage: SecureStorage
  readonly BackButton: BackButton
  readonly BiometricManager: BiometricManager
  readonly HapticFeedback: HapticFeedback
  readonly ScreenCapture: ScreenCapture
  readonly swipesBehaviorManager: SwipesBehavior

  // Методы API
  ready: () => void
  close: () => void

  postEvent: (event: string, data?: any, callback?: () => void) => void

  requestScreenMaxBrightness: () => Promise<any>
  restoreScreenBrightness: () => Promise<any>

  requestContact: () => Promise<any>

  enableClosingConfirmation: () => void
  disableClosingConfirmation: () => void

  openLink: (url: string) => void
  openMaxLink: (url: string) => void

  downloadFile: (url: string, file_name?: string) => Promise<any>

  shareContent: (data: any) => Promise<any>
  shareMaxContent: (data: any) => Promise<any>

  enableVerticalSwipes: () => Promise<any>
  disableVerticalSwipes: () => Promise<any>

  openCodeReader: (fileSelect?: boolean) => Promise<any>
}

declare global {
  interface Window {
    WebApp: WebApp
  }
}
