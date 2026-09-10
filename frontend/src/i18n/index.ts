import en from './locales/en.json';
import hi from './locales/hi.json';
import hinglish from './locales/hinglish.json';

export type SupportedLanguage = 'en' | 'hi' | 'hinglish';

export const locales = {
  en,
  hi,
  hinglish
} as const;

export function getTranslation(lang: SupportedLanguage = 'hi') {
  return locales[lang] || locales.hi;
}

export function t(keyPath: string, lang: SupportedLanguage = 'hi'): string {
  const dict = getTranslation(lang);
  const keys = keyPath.split('.');
  let current: any = dict;

  for (const k of keys) {
    if (current && typeof current === 'object' && k in current) {
      current = current[k];
    } else {
      return keyPath;
    }
  }

  return typeof current === 'string' ? current : keyPath;
}
