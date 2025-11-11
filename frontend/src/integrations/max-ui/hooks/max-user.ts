export type MaxUser = {
  id: number
  firstName: string
  lastName: string
  username: string
  photoUrl: string
}

export function useMaxUser(): MaxUser {
  return {
    id: 4,
    firstName: 'Daniil',
    lastName: 'Doe',
    username: 'johndoe',
    photoUrl: 'https://example.com/photo.jpg',
  }
}
