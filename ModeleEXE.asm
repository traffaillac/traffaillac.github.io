;##############################################################################
; Fichier : ModeleEXE.inc
; Auteur : Thibault Raffaillac <thibaultraffaillac@yahoo.fr>
; Création le : 18/06/08
; Dernière modification le : 18/06/08
;
; Ce fichier contient tous les outils nécessaires pour créer manuellement un
; fichier .exe avec nasm. Il faut utiliser l'option -fbin de nasm.
;##############################################################################

;==============================================================================
; Définition des constantes de précompilation qui seront utilisées pour
; fabriquer l'en-tête
;------------------------------------------------------------------------------
%define TAILLE_CODE_MEM (((finCode-debutCode+0FFFh)>>12)<<12)
%define TAILLE_CODE_FICH (((finCode-debutCode+1FFh)>>9)<<9)
%define TAILLE_DONNEES_MEM (((finDonnees-debutDonnees+0FFFh)>>12)<<12)
%define TAILLE_DONNEES_FICH (((finDonnees-debutDonnees+1FFh)>>9)<<9)
%define TAILLE_BSS_MEM (((finBSS-debutBSS+0FFFh)>>12)<<12)
%define TAILLE_BSS_FICH (((finBSS-debutBSS+1FFh)>>9)<<9)
%define TAILLE_EN_TETE_MEM (((finEnTete-enTeteDOS+0FFFh)>>12)<<12)
%define TAILLE_EN_TETE_FICH (((finEnTete-enTeteDOS+1FFh)>>9)<<9)
%define TAILLE_TOTALE_MEM (TAILLE_EN_TETE_MEM+TAILLE_CODE_MEM+\
   TAILLE_DONNEES_MEM+TAILLE_BSS_MEM)
%define ADRESSE_CHARGEMENT_CODE 1000h
%define ADRESSE_CHARGEMENT_DONNEES 2000h
%define ADRESSE_CHARGEMENT_BSS 3000h
%define NOMBRE_SECTIONS 3

;==============================================================================
; En-tête MS-DOS (copié sur des en-têtes existants)
;------------------------------------------------------------------------------
enTeteDOS:
            dw 5A4Dh       ; signature, indique que le fichier est un exécutable
            dw 0090h       ; ?
            dw 0003h       ; ?
            dw 0000h       ; nombre de relocalisations
            dw 0004h       ; taille de l'en-tête DOS en paragraphes (16 octets)
            dw 0000h       ; ?
            dw 0FFFFh      ; ?
            dw 0000h       ; valeur initiale de SS
            dw 00B8h       ; valeur initiale de SP
            dw 0000h       ; somme de contrôle (checksum)
            dw 0000h       ; valeur initiale de IP (après l'en-tête DOS)
            dw 0000h       ; valeur initiale de CS
            dw 0040h       ; adresse du tableau des relocalisations
            dw 0000h       ; ?
TIMES 3Ch-($-$$) db 0      ; sections réservées
            dd enTeteCOFF  ; adresse de l'en-tête EXE
;------------------------------------------------------------------------------
; Programme MS-DOS (copié sur des en-têtes existants)
;------------------------------------------------------------------------------
BITS 16
      push cs
      pop ds
      mov dx, 000Eh
      mov ah, 0009h
      int 21h           ; interruption 9 qui affiche à l'écran le texte en DS:DX
      mov ax, 4C01h
      int 21h           ; interruption 4C qui met fin au programme
            db 'This program cannot be run in DOS mode.',0Dh,0Ah,'$'
ALIGN 16, db 0 ; alignement sur la prochaine
               ; frontière de 16 octets

;==============================================================================
; En-tête de fichier COFF (basé sur la spécification officielle)
;------------------------------------------------------------------------------
enTeteCOFF:
            db 'PE',0,0    ; signature (format Portable Executable)
            dw 14ch        ; machine (intel 386 et compatibles)
            dw NOMBRE_SECTIONS ; nombre de sections
            dd __POSIX_TIME__ ; date de création du fichier
            dd 00000000h   ; inutile pour un exécutable
            dd 00000000h   ; inutile pour un exécutable
            dw listeSections-enTeteOptionnel ; taille de l'en-tête optionnel
            dw 0303h       ; caractéristiques : _ pas de relocalisations
                           ;                    _ n'est pas un fichier objet
                           ;                    _ conçu pour une machine 32-bits
                           ;                    _ pas d'informations de débogage

;==============================================================================
; En-tête optionnel (basé sur la spécification officielle)
;------------------------------------------------------------------------------
enTeteOptionnel:
            dw 010Bh       ; nombre magique, indique la version de l'en-tête
                           ; de l'en-tête optionnel (PE32)
            db 00h         ; numéro majeur de version du lieur
            db 00h         ; numéro mineur de version du lieur
            dd TAILLE_CODE_FICH ; taille totale des sections contenant du code
                           ; exécutable dans le fichier (multiple de la taille
                           ; d'une section dans le fichier)
            dd TAILLE_DONNEES_FICH ; taille totale des sections de données
                           ; initialisées (import comprises) dans le fichier
            dd TAILLE_BSS_FICH ; taille totale des sections de données non
                           ; initialisées dans le fichier
            dd main-00400000h ; point de départ du programme, par rapport au
                           ; point de chargement du programme
            dd ADRESSE_CHARGEMENT_CODE ; ?, semble indiquer la plus petite
                           ; adresse relative d'un segment de code chargé
                           ; en mémoire
            dd ADRESSE_CHARGEMENT_DONNEES ; ?, semble indiquer la plus petite
                           ; adresse relative d'un segment de données chargé
                           ; en mémoire
            dd 00400000h   ; adresse dans la mémoire virtuelle allouée par l'OS
                           ; où charger le programme
            dd 1000h       ; taille en octets des sections chargées en mémoire,
                           ; fixée ici à la taille de pagination du processeur
            dd 200h        ; taille des sections stockées dans le fichier EXE,
                           ; fixé ici à la plus petite taille autorisée
            dw 0004h       ; le numéro majeur de version de l'OS requis
            dw 0000h       ; le numéro mineur de version de l'OS requis
            dw 0000h       ; ?, numéro majeur de l'exécutable
            dw 0000h       ; ?, numéro mineur de l'exécutable
            dw 0004h       ; le numéro majeur de version du sous-système requis
            dw 0000h       ; le numéro mineur de version du sous-système requis
            dd 0000h       ; réservé (doit valoir 0)
            dd TAILLE_TOTALE_MEM ; taille en octets de l'ensemble des sections
                           ; chargées en mémoire (multiple de la taille d'une
                           ; section dans la mémoire)
            dd TAILLE_EN_TETE_FICH ; taille de tous les en-têtes (DOS, PE et de
                           ; sections) en multiple de la taille d'une section
                           ; dans le fichier)
            dd 00000000h   ; somme de contrôle, n'est contrôlée que pour les
                           ; fichiers lancés au démarrage et les pilotes
            dw 0003h       ; le sous-système pour lequel ce programme est
                           ; conçu : _ 0002h=Windows GUI (affichage graphique)
                           ;         _ 0003h=Windows CUI (console)
            dw 0000h       ; caractéristiques si le fichier était une DLL
            dd 00100000h   ; taille totale de la pile à allouer en mémoire
            dd 00001000h   ; taille de la pile à allouer au démarrage du
                           ; programme (le reste viendra avec la demande)
            dd 00100000h   ; ?, allocation totale du tas (heap)
            dd 00001000h   ; ?, allocation du tas au démarrage
            dd 00000000h   ; réservé (doit valoir 0)
            dd 00000010h   ; nombre de couples {adresse virtuelle, taille} dans
                           ; la dernière partie de l'en-tête optionnel
            
;==============================================================================
; Adresses et tailles des tableaux d'informations supplémentaires (dernière
; partie de l'en-tête optionnel, basé sur la spécification standard)
; L'adresse virtuelle relative désigne une adresse en mémoire par rapport au
; point de départ où est chargé le programme.
;------------------------------------------------------------------------------
; tableau des exportations de symboles (section .edata)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des importations de symboles (section .idata)
            dd repertoireImport-00400000h ; adresse virtuelle relative
            dd listeAdressesImports-repertoireImport ; taille du tableau
; tableau des ressources incluses dans le fichier (section .rsrc)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des fonctions gérant les exceptions (section .pdata)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des certificats
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des relocalisations de symboles (section .reloc)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des informations de débogage (section .debug)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau réservé
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; adresse de la valeur à placer dans le registre de pointeur global
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; doit valoir 0
; tableau de stockage des variables locales des threads (section .tls)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau de chargement de configuration
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; ?, tableau de "bound import"
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des adresses de symboles importés
; Le contenu de ce tableau est initialement identique à la liste des symboles à
; importer, puis l'OS le met à jour losqu'il charge ces symboles en mémoire.
            dd listeAdressesImports-00400000h ; adresse virtuelle relative
            dd listeImports-listeAdressesImports ; taille du tableau
; tableau des importations retardées de symboles
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; en-tête CLR (utile aux fichiers objets uniquement, section .cormeta)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; couple vide
            dd 00000000h   ; doit valoir 0
            dd 00000000h   ; doit valoir 0

;==============================================================================
; Liste des sections (basée sur la spécification officielle)
; Ces descriptifs de sections doivent apparaître dans l'ordre dans lequel elles
; seront chargées en mémoire.
;------------------------------------------------------------------------------
listeSections:
; Section contenant le code exécutable
            db '.text',0,0,0 ; nom de la section, sur 8 octets
            dd finCode-debutCode ; taille totale de la section lorsqu'elle est
                           ; chargée en mémoire, sans compter les zéros ajoutés
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_CODE ; adresse virtuelle relative où est
                           ; chargée la section
            dd TAILLE_CODE_FICH ; taille des données de la section présentes
                           ; dans le fichier, en comptant les zéros ajoutés
            dd section.code.start ; adresse dans le fichier de la section
                           ; à charger
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dd 60000020h   ; caractéristiques de la section :
                           ; _ 00000020h=contient du code exécutable
                           ; _ 20000000h=ses données peuvent être exécutées
                           ; _ 40000000h=ses données peuvent être lues
; Section contenant les données initialisées
            db '.data',0,0,0 ; nom de la section, sur 8 octets
            dd finDonnees-debutDonnees ; taille totale de la section
                           ; en mémoire, sans compter les zéros ajoutés
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_DONNEES ; adresse virtuelle relative où est
                           ; chargée la section
            dd TAILLE_DONNEES_FICH ; taille des données de la section présentes
                           ; dans le fichier, en comptant les zéros ajoutés
            dd section.donnees.start ; adresse dans le fichier de la section
                           ; à charger
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dd 0C0000040h  ; caractéristiques de la section :
                           ; _ 00000040h=contient des données initialisées
                           ; _ 40000000h=ses données peuvent être lues
                           ; _ 80000000h=ses données peuvent être réécrites
; Section contenant les données non initialisées
            db '.bss',0,0,0,0 ; nom de la section, sur 8 octets
            dd finBSS-debutBSS ; taille totale de la section losqu'elle est
                           ; chargée en mémoire, sans compter les zéros ajoutés
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_BSS ; adresse virtuelle relative où est
                           ; chargée la section
            dd TAILLE_BSS_FICH ; taille des données de la section présentes
                           ; dans le fichier, en comptant les zéros ajoutés
            dd section.bss.start ; adresse dans le fichier de la section
                           ; à charger
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dd 00000000h   ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dw 0000h       ; inutile pour un exécutable (doit valoir 0)
            dd 0C0000080h  ; caractéristiques de la section :
                           ; _ 00000080h=contient des données non initialisées
                           ; _ 40000000h=ses données peuvent être lues
                           ; _ 80000000h=ses données peuvent être réécrites
finEnTete:

;==============================================================================
; Définition des sections utilisées par nasm
; Toutes les instructions précédentes appartiennent implicitement à la section
; .text.
;------------------------------------------------------------------------------
SECTION code progbits align=200h follows=.text vstart=00400000h+ADRESSE_CHARGEMENT_CODE
debutCode:
SECTION donnees progbits align=200h follows=code vstart=00400000h+ADRESSE_CHARGEMENT_DONNEES
debutDonnees:
SECTION bss nobits vstart=00400000h+ADRESSE_CHARGEMENT_BSS
debutBSS:

;##############################################################################
; Le corps du programme commence ici.
;==============================================================================
SECTION code
BITS 32
main:



push dword 0
call [ExitProcess]
;==============================================================================
; Le corps du programme s'arrête ici.
;##############################################################################

SECTION donnees
;==============================================================================
; Tableau du répertoire des symboles à importer
;------------------------------------------------------------------------------
repertoireImport:
; KERNEL32
            dd listeImports-00400000h ; adresse de la liste des symboles
                                      ; importés
            dd 00000000h   ; réservé (doit valoir 0)
            dd 00000000h   ; ?
            dd KERNEL32-00400000h ; adresse du nom de la DLL en chaîne ASCII
            dd listeAdressesImports-00400000h ; adresse de la liste des
                           ; adresses des symboles importés, mise à jour par
                           ; l'OS lors du chargement du programme
; Dernière entrée vide
TIMES 5     dd 00000000h

;==============================================================================
; Liste des adresses des symboles importés, identique à la liste des symboles
; à importer jusqu'à ce que l'OS la mette à jour avec des adresses en mémoire
;------------------------------------------------------------------------------
listeAdressesImports:
; KERNEL32
ExitProcess dd nomExitProcess-00400000h ; adresse du nom de la fonction
; Dernière entrée vide
            dd 00000000h

;==============================================================================
; Liste des symboles à importer
; Le bit de poids fort est toujours fixé à 0 pour indiquer que les symboles
; doivent être importés par nom.
;------------------------------------------------------------------------------
listeImports:
; KERNEL32
            dd nomExitProcess-00400000h ; adresse du nom de la fonction
; Dernière entrée vide
            dd 00000000h

;==============================================================================
; Tableau des noms des DLL importées
;------------------------------------------------------------------------------
KERNEL32    db 'KERNEL32.DLL',0

;==============================================================================
; Tableau des noms des symboles à importer
; Le premier nombre est l'index du symbole dans le tableau des exportations de
; la DLL visée.
;------------------------------------------------------------------------------
TIMES (((($-$$)+1)>>1)<<1)-($-$$) db 0
nomExitProcess dw 00B7h       ; index
            db 'ExitProcess',0

;==============================================================================
; Définition des derniers labels pour finaliser le programme
;------------------------------------------------------------------------------
SECTION code
finCode:
SECTION donnees
finDonnees:
TIMES (((($-$$)+1FFh)>>9)<<9)-($-$$) db 0
SECTION bss
finBSS:











; A ne pas oublier :
; _ Remplir le reste de la section donnees par des zéros si nécessaire.






















