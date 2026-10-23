/*
 * kbd.h — Windows klaviatura layout DLL (kbd*.dll) uchun minimal sarlavha.
 *
 * Bu fayl WDK'dagi kbd.h ning faqat kerakli qismini mustaqil (windows.h'siz)
 * ko'rinishda qayta yozadi, shuning uchun layout DLL'lari mingw-w64 bilan
 * (Linux/Windows'da) -nostdlib rejimida yig'iladi.
 *
 * Tuzilmalar xotirada WDK'dagi bilan bir xil joylashgan (x86 va x64).
 */
#ifndef UZ_KBD_H
#define UZ_KBD_H

typedef unsigned char  BYTE;
typedef unsigned short WORD;
typedef unsigned short WCHAR;
typedef unsigned int   DWORD;   /* 32 bit */

#ifndef NULL
#  define NULL ((void *)0)
#endif

#if defined(_WIN32)
#  define KBD_EXPORT __declspec(dllexport)
#else
#  define KBD_EXPORT
#endif

/* ---- Virtual-key kodlari (winuser.h) ------------------------------------ */
#define VK_CANCEL 0x03
#define VK_BACK 0x08
#define VK_TAB 0x09
#define VK_CLEAR 0x0C
#define VK_RETURN 0x0D
#define VK_SHIFT 0x10
#define VK_CONTROL 0x11
#define VK_MENU 0x12
#define VK_PAUSE 0x13
#define VK_CAPITAL 0x14
#define VK_ESCAPE 0x1B
#define VK_SPACE 0x20
#define VK_PRIOR 0x21
#define VK_NEXT 0x22
#define VK_END 0x23
#define VK_HOME 0x24
#define VK_LEFT 0x25
#define VK_UP 0x26
#define VK_RIGHT 0x27
#define VK_DOWN 0x28
#define VK_SNAPSHOT 0x2C
#define VK_INSERT 0x2D
#define VK_DELETE 0x2E
#define VK_LWIN 0x5B
#define VK_RWIN 0x5C
#define VK_APPS 0x5D
#define VK_SLEEP 0x5F
#define VK_NUMPAD0 0x60
#define VK_NUMPAD1 0x61
#define VK_NUMPAD2 0x62
#define VK_NUMPAD3 0x63
#define VK_NUMPAD4 0x64
#define VK_NUMPAD5 0x65
#define VK_NUMPAD6 0x66
#define VK_NUMPAD7 0x67
#define VK_NUMPAD8 0x68
#define VK_NUMPAD9 0x69
#define VK_MULTIPLY 0x6A
#define VK_ADD 0x6B
#define VK_SUBTRACT 0x6D
#define VK_DECIMAL 0x6E
#define VK_DIVIDE 0x6F
#define VK_F1 0x70
#define VK_F2 0x71
#define VK_F3 0x72
#define VK_F4 0x73
#define VK_F5 0x74
#define VK_F6 0x75
#define VK_F7 0x76
#define VK_F8 0x77
#define VK_F9 0x78
#define VK_F10 0x79
#define VK_F11 0x7A
#define VK_F12 0x7B
#define VK_F13 0x7C
#define VK_F14 0x7D
#define VK_F15 0x7E
#define VK_F16 0x7F
#define VK_F17 0x80
#define VK_F18 0x81
#define VK_F19 0x82
#define VK_F20 0x83
#define VK_F21 0x84
#define VK_F22 0x85
#define VK_F23 0x86
#define VK_F24 0x87
#define VK_NUMLOCK 0x90
#define VK_SCROLL 0x91
#define VK_LSHIFT 0xA0
#define VK_RSHIFT 0xA1
#define VK_LCONTROL 0xA2
#define VK_RCONTROL 0xA3
#define VK_LMENU 0xA4
#define VK_RMENU 0xA5
#define VK_BROWSER_BACK 0xA6
#define VK_BROWSER_FORWARD 0xA7
#define VK_BROWSER_REFRESH 0xA8
#define VK_BROWSER_STOP 0xA9
#define VK_BROWSER_SEARCH 0xAA
#define VK_BROWSER_FAVORITES 0xAB
#define VK_BROWSER_HOME 0xAC
#define VK_VOLUME_MUTE 0xAD
#define VK_VOLUME_DOWN 0xAE
#define VK_VOLUME_UP 0xAF
#define VK_MEDIA_NEXT_TRACK 0xB0
#define VK_MEDIA_PREV_TRACK 0xB1
#define VK_MEDIA_STOP 0xB2
#define VK_MEDIA_PLAY_PAUSE 0xB3
#define VK_LAUNCH_MAIL 0xB4
#define VK_LAUNCH_MEDIA_SELECT 0xB5
#define VK_LAUNCH_APP1 0xB6
#define VK_LAUNCH_APP2 0xB7
#define VK_OEM_1 0xBA
#define VK_OEM_PLUS 0xBB
#define VK_OEM_COMMA 0xBC
#define VK_OEM_MINUS 0xBD
#define VK_OEM_PERIOD 0xBE
#define VK_OEM_2 0xBF
#define VK_OEM_3 0xC0
#define VK_ABNT_C1 0xC1
#define VK_ABNT_C2 0xC2
#define VK_OEM_4 0xDB
#define VK_OEM_5 0xDC
#define VK_OEM_6 0xDD
#define VK_OEM_7 0xDE
#define VK_OEM_8 0xDF
#define VK_OEM_102 0xE2

/* ---- Skan-kod -> VK jadvali bayroqlari ---------------------------------- */
#define KBDEXT      0x0100
#define KBDMULTIVK  0x0200
#define KBDSPECIAL  0x0400
#define KBDNUMPAD   0x0800

/* ---- Modifikatorlar ----------------------------------------------------- */
#define KBDBASE   0
#define KBDSHIFT  0x01
#define KBDCTRL   0x02
#define KBDALT    0x04
#define SHFT_INVALID 0x0F

/* ---- VK_TO_WCHARS atributlari ------------------------------------------- */
#define CAPLOK      0x01
#define SGCAPS      0x02
#define CAPLOKALTGR 0x04

#define WCH_NONE 0xF000
#define WCH_DEAD 0xF001
#define WCH_LGTR 0xF002

/* ---- Locale bayroqlari -------------------------------------------------- */
#define KLLF_ALTGR     0x0001
#define KBD_VERSION    1
#define MAKELONG(lo, hi) ((DWORD)(((WORD)(lo)) | (((DWORD)((WORD)(hi))) << 16)))

/* ---- Tuzilmalar --------------------------------------------------------- */
typedef struct { BYTE Vk; BYTE ModBits; } VK_TO_BIT;

typedef struct {
    VK_TO_BIT *pVkToBit;
    WORD       wMaxModBits;
    BYTE       ModNumber[8];          /* wMaxModBits + 1 ta element */
} MODIFIERS;

#define DEFINE_VK_TO_WCHARS(n)                         \
    typedef struct {                                   \
        BYTE  VirtualKey;                              \
        BYTE  Attributes;                              \
        WCHAR wch[n];                                  \
    } VK_TO_WCHARS##n

DEFINE_VK_TO_WCHARS(1);
DEFINE_VK_TO_WCHARS(5);

typedef struct {
    VK_TO_WCHARS1 *pVkToWchars;
    BYTE           nModifications;
    BYTE           cbSize;
} VK_TO_WCHAR_TABLE;

typedef struct { BYTE Vsc; WORD Vk; } VSC_VK;                 /* skan-kod -> VK (E0/E1 jadvallari) */
typedef struct { BYTE Vsc; WCHAR *pwsz; } VSC_LPWSTR;         /* tugma nomlari */

/* Ushbu layoutlarda o'lik tugmalar (dead key) va ligaturalar yo'q — NULL. */
typedef struct tagKbdLayer {
    MODIFIERS          *pCharModifiers;
    VK_TO_WCHAR_TABLE  *pVkToWcharTable;
    void               *pDeadKey;
    VSC_LPWSTR         *pKeyNames;
    VSC_LPWSTR         *pKeyNamesExt;
    WCHAR             **pKeyNamesDead;
    WORD               *pusVSCtoVK;
    BYTE                bMaxVSCtoVK;
    VSC_VK             *pVSCtoVK_E0;
    VSC_VK             *pVSCtoVK_E1;
    DWORD               fLocaleFlags;
    BYTE                nLgMax;
    BYTE                cbLgEntry;
    void               *pLigature;
    DWORD               dwType;
    DWORD               dwSubType;
} KBDTABLES;

#endif /* UZ_KBD_H */
