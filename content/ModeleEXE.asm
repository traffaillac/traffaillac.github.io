;##############################################################################
; Fichier : ModeleEXE.inc
; Auteur : Thibault Raffaillac <thibaultraffaillac@yahoo.fr>
; Cr�ation le : 18/06/08
; Derni�re modification le : 18/06/08
;
; Ce fichier contient tous les outils n�cessaires pour cr�er manuellement un
; fichier .exe avec nasm. Il faut utiliser l'option -fbin de nasm.
;##############################################################################

;==============================================================================
; D�finition des constantes de pr�compilation qui seront utilis�es pour
; fabriquer l'en-t�te
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
; En-t�te MS-DOS (copi� sur des en-t�tes existants)
;------------------------------------------------------------------------------
enTeteDOS:
            dw 5A4Dh       ; signature, indique que le fichier est un ex�cutable
            dw 0090h       ; ?
            dw 0003h       ; ?
            dw 0000h       ; nombre de relocalisations
            dw 0004h       ; taille de l'en-t�te DOS en paragraphes (16 octets)
            dw 0000h       ; ?
            dw 0FFFFh      ; ?
            dw 0000h       ; valeur initiale de SS
            dw 00B8h       ; valeur initiale de SP
            dw 0000h       ; somme de contr�le (checksum)
            dw 0000h       ; valeur initiale de IP (apr�s l'en-t�te DOS)
            dw 0000h       ; valeur initiale de CS
            dw 0040h       ; adresse du tableau des relocalisations
            dw 0000h       ; ?
TIMES 3Ch-($-$$) db 0      ; sections r�serv�es
            dd enTeteCOFF  ; adresse de l'en-t�te EXE
;------------------------------------------------------------------------------
; Programme MS-DOS (copi� sur des en-t�tes existants)
;------------------------------------------------------------------------------
BITS 16
      push cs
      pop ds
      mov dx, 000Eh
      mov ah, 0009h
      int 21h           ; interruption 9 qui affiche � l'�cran le texte en DS:DX
      mov ax, 4C01h
      int 21h           ; interruption 4C qui met fin au programme
            db 'This program cannot be run in DOS mode.',0Dh,0Ah,'$'
ALIGN 16, db 0 ; alignement sur la prochaine
               ; fronti�re de 16 octets

;==============================================================================
; En-t�te de fichier COFF (bas� sur la sp�cification officielle)
;------------------------------------------------------------------------------
enTeteCOFF:
            db 'PE',0,0    ; signature (format Portable Executable)
            dw 14ch        ; machine (intel 386 et compatibles)
            dw NOMBRE_SECTIONS ; nombre de sections
            dd __POSIX_TIME__ ; date de cr�ation du fichier
            dd 00000000h   ; inutile pour un ex�cutable
            dd 00000000h   ; inutile pour un ex�cutable
            dw listeSections-enTeteOptionnel ; taille de l'en-t�te optionnel
            dw 0303h       ; caract�ristiques : _ pas de relocalisations
                           ;                    _ n'est pas un fichier objet
                           ;                    _ con�u pour une machine 32-bits
                           ;                    _ pas d'informations de d�bogage

;==============================================================================
; En-t�te optionnel (bas� sur la sp�cification officielle)
;------------------------------------------------------------------------------
enTeteOptionnel:
            dw 010Bh       ; nombre magique, indique la version de l'en-t�te
                           ; de l'en-t�te optionnel (PE32)
            db 00h         ; num�ro majeur de version du lieur
            db 00h         ; num�ro mineur de version du lieur
            dd TAILLE_CODE_FICH ; taille totale des sections contenant du code
                           ; ex�cutable dans le fichier (multiple de la taille
                           ; d'une section dans le fichier)
            dd TAILLE_DONNEES_FICH ; taille totale des sections de donn�es
                           ; initialis�es (import comprises) dans le fichier
            dd TAILLE_BSS_FICH ; taille totale des sections de donn�es non
                           ; initialis�es dans le fichier
            dd main-00400000h ; point de d�part du programme, par rapport au
                           ; point de chargement du programme
            dd ADRESSE_CHARGEMENT_CODE ; ?, semble indiquer la plus petite
                           ; adresse relative d'un segment de code charg�
                           ; en m�moire
            dd ADRESSE_CHARGEMENT_DONNEES ; ?, semble indiquer la plus petite
                           ; adresse relative d'un segment de donn�es charg�
                           ; en m�moire
            dd 00400000h   ; adresse dans la m�moire virtuelle allou�e par l'OS
                           ; o� charger le programme
            dd 1000h       ; taille en octets des sections charg�es en m�moire,
                           ; fix�e ici � la taille de pagination du processeur
            dd 200h        ; taille des sections stock�es dans le fichier EXE,
                           ; fix� ici � la plus petite taille autoris�e
            dw 0004h       ; le num�ro majeur de version de l'OS requis
            dw 0000h       ; le num�ro mineur de version de l'OS requis
            dw 0000h       ; ?, num�ro majeur de l'ex�cutable
            dw 0000h       ; ?, num�ro mineur de l'ex�cutable
            dw 0004h       ; le num�ro majeur de version du sous-syst�me requis
            dw 0000h       ; le num�ro mineur de version du sous-syst�me requis
            dd 0000h       ; r�serv� (doit valoir 0)
            dd TAILLE_TOTALE_MEM ; taille en octets de l'ensemble des sections
                           ; charg�es en m�moire (multiple de la taille d'une
                           ; section dans la m�moire)
            dd TAILLE_EN_TETE_FICH ; taille de tous les en-t�tes (DOS, PE et de
                           ; sections) en multiple de la taille d'une section
                           ; dans le fichier)
            dd 00000000h   ; somme de contr�le, n'est contr�l�e que pour les
                           ; fichiers lanc�s au d�marrage et les pilotes
            dw 0003h       ; le sous-syst�me pour lequel ce programme est
                           ; con�u : _ 0002h=Windows GUI (affichage graphique)
                           ;         _ 0003h=Windows CUI (console)
            dw 0000h       ; caract�ristiques si le fichier �tait une DLL
            dd 00100000h   ; taille totale de la pile � allouer en m�moire
            dd 00001000h   ; taille de la pile � allouer au d�marrage du
                           ; programme (le reste viendra avec la demande)
            dd 00100000h   ; ?, allocation totale du tas (heap)
            dd 00001000h   ; ?, allocation du tas au d�marrage
            dd 00000000h   ; r�serv� (doit valoir 0)
            dd 00000010h   ; nombre de couples {adresse virtuelle, taille} dans
                           ; la derni�re partie de l'en-t�te optionnel
            
;==============================================================================
; Adresses et tailles des tableaux d'informations suppl�mentaires (derni�re
; partie de l'en-t�te optionnel, bas� sur la sp�cification standard)
; L'adresse virtuelle relative d�signe une adresse en m�moire par rapport au
; point de d�part o� est charg� le programme.
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
; tableau des fonctions g�rant les exceptions (section .pdata)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des certificats
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des relocalisations de symboles (section .reloc)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau des informations de d�bogage (section .debug)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; tableau r�serv�
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; adresse de la valeur � placer dans le registre de pointeur global
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
; tableau des adresses de symboles import�s
; Le contenu de ce tableau est initialement identique � la liste des symboles �
; importer, puis l'OS le met � jour losqu'il charge ces symboles en m�moire.
            dd listeAdressesImports-00400000h ; adresse virtuelle relative
            dd listeImports-listeAdressesImports ; taille du tableau
; tableau des importations retard�es de symboles
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; en-t�te CLR (utile aux fichiers objets uniquement, section .cormeta)
            dd 00000000h   ; adresse virtuelle relative
            dd 00000000h   ; taille du tableau
; couple vide
            dd 00000000h   ; doit valoir 0
            dd 00000000h   ; doit valoir 0

;==============================================================================
; Liste des sections (bas�e sur la sp�cification officielle)
; Ces descriptifs de sections doivent appara�tre dans l'ordre dans lequel elles
; seront charg�es en m�moire.
;------------------------------------------------------------------------------
listeSections:
; Section contenant le code ex�cutable
            db '.text',0,0,0 ; nom de la section, sur 8 octets
            dd finCode-debutCode ; taille totale de la section lorsqu'elle est
                           ; charg�e en m�moire, sans compter les z�ros ajout�s
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_CODE ; adresse virtuelle relative o� est
                           ; charg�e la section
            dd TAILLE_CODE_FICH ; taille des donn�es de la section pr�sentes
                           ; dans le fichier, en comptant les z�ros ajout�s
            dd section.code.start ; adresse dans le fichier de la section
                           ; � charger
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dd 60000020h   ; caract�ristiques de la section :
                           ; _ 00000020h=contient du code ex�cutable
                           ; _ 20000000h=ses donn�es peuvent �tre ex�cut�es
                           ; _ 40000000h=ses donn�es peuvent �tre lues
; Section contenant les donn�es initialis�es
            db '.data',0,0,0 ; nom de la section, sur 8 octets
            dd finDonnees-debutDonnees ; taille totale de la section
                           ; en m�moire, sans compter les z�ros ajout�s
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_DONNEES ; adresse virtuelle relative o� est
                           ; charg�e la section
            dd TAILLE_DONNEES_FICH ; taille des donn�es de la section pr�sentes
                           ; dans le fichier, en comptant les z�ros ajout�s
            dd section.donnees.start ; adresse dans le fichier de la section
                           ; � charger
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dd 0C0000040h  ; caract�ristiques de la section :
                           ; _ 00000040h=contient des donn�es initialis�es
                           ; _ 40000000h=ses donn�es peuvent �tre lues
                           ; _ 80000000h=ses donn�es peuvent �tre r��crites
; Section contenant les donn�es non initialis�es
            db '.bss',0,0,0,0 ; nom de la section, sur 8 octets
            dd finBSS-debutBSS ; taille totale de la section losqu'elle est
                           ; charg�e en m�moire, sans compter les z�ros ajout�s
                           ; pour respecter la taille de section du fichier
            dd ADRESSE_CHARGEMENT_BSS ; adresse virtuelle relative o� est
                           ; charg�e la section
            dd TAILLE_BSS_FICH ; taille des donn�es de la section pr�sentes
                           ; dans le fichier, en comptant les z�ros ajout�s
            dd section.bss.start ; adresse dans le fichier de la section
                           ; � charger
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dd 00000000h   ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dw 0000h       ; inutile pour un ex�cutable (doit valoir 0)
            dd 0C0000080h  ; caract�ristiques de la section :
                           ; _ 00000080h=contient des donn�es non initialis�es
                           ; _ 40000000h=ses donn�es peuvent �tre lues
                           ; _ 80000000h=ses donn�es peuvent �tre r��crites
finEnTete:

;==============================================================================
; D�finition des sections utilis�es par nasm
; Toutes les instructions pr�c�dentes appartiennent implicitement � la section
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
; Le corps du programme s'arr�te ici.
;##############################################################################

SECTION donnees
;==============================================================================
; Tableau du r�pertoire des symboles � importer
;------------------------------------------------------------------------------
repertoireImport:
; KERNEL32
            dd listeImports-00400000h ; adresse de la liste des symboles
                                      ; import�s
            dd 00000000h   ; r�serv� (doit valoir 0)
            dd 00000000h   ; ?
            dd KERNEL32-00400000h ; adresse du nom de la DLL en cha�ne ASCII
            dd listeAdressesImports-00400000h ; adresse de la liste des
                           ; adresses des symboles import�s, mise � jour par
                           ; l'OS lors du chargement du programme
; Derni�re entr�e vide
TIMES 5     dd 00000000h

;==============================================================================
; Liste des adresses des symboles import�s, identique � la liste des symboles
; � importer jusqu'� ce que l'OS la mette � jour avec des adresses en m�moire
;------------------------------------------------------------------------------
listeAdressesImports:
; KERNEL32
ExitProcess dd nomExitProcess-00400000h ; adresse du nom de la fonction
; Derni�re entr�e vide
            dd 00000000h

;==============================================================================
; Liste des symboles � importer
; Le bit de poids fort est toujours fix� � 0 pour indiquer que les symboles
; doivent �tre import�s par nom.
;------------------------------------------------------------------------------
listeImports:
; KERNEL32
            dd nomExitProcess-00400000h ; adresse du nom de la fonction
; Derni�re entr�e vide
            dd 00000000h

;==============================================================================
; Tableau des noms des DLL import�es
;------------------------------------------------------------------------------
KERNEL32    db 'KERNEL32.DLL',0

;==============================================================================
; Tableau des noms des symboles � importer
; Le premier nombre est l'index du symbole dans le tableau des exportations de
; la DLL vis�e.
;------------------------------------------------------------------------------
TIMES (((($-$$)+1)>>1)<<1)-($-$$) db 0
nomExitProcess dw 00B7h       ; index
            db 'ExitProcess',0

;==============================================================================
; D�finition des derniers labels pour finaliser le programme
;------------------------------------------------------------------------------
SECTION code
finCode:
SECTION donnees
finDonnees:
TIMES (((($-$$)+1FFh)>>9)<<9)-($-$$) db 0
SECTION bss
finBSS:











; A ne pas oublier :
; _ Remplir le reste de la section donnees par des z�ros si n�cessaire.






















