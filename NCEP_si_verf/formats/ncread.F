      PROGRAM ncread
! read netcdf ncar file
! Robert Grumbine
      USE netcdf

      IMPLICIT none

      INTEGER nx, ny
      PARAMETER (nx = 360)
      PARAMETER (ny = 359)
      REAL aice(nx, ny), hi(nx, ny), hs(nx, ny), Tsfc(nx, ny)
      REAL uvel(nx, ny), vvel(nx, ny), sst(nx, ny)
      REAL tlat(nx, ny), tlon(nx, ny)
      CHARACTER*90 fname
      
      INTEGER :: ncid, varid(7)
      INTEGER :: r1, r2, r3

      INTEGER i, j

! Open the netcdf file, and check result code
      r1 = nf90_open("shan.nc", NF90_NOWRITE, ncid) 
      CALL check(r1)

! Get variable id number and check return
! valid vars are: hi, hs, Tsfc, aice, uvel, vvel, sst (among others)
      r2 = nf90_inq_varid(ncid, "aice_d", varid(1)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "hi_d", varid(2)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "hs_d", varid(3)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "Tsfc_d", varid(4)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "sst_d", varid(5)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "TLAT", varid(6)) 
      CALL check(r2)
      r2 = nf90_inq_varid(ncid, "TLON", varid(7)) 
      CALL check(r2)

! Finally, get the data element and check return code
      r3 = nf90_get_var(ncid, varid(1), aice) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(2), hi) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(3), hs) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(4), Tsfc) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(5), sst) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(6), tlat) 
      CALL check(r3)
      r3 = nf90_get_var(ncid, varid(7), tlon) 
      CALL check(r3)

!nonvals (prior to rescaling) are -30000s
!      aice = aice * 0.0001
!      hi   = hi   * 0.001
!      hs   = hs   * 0.001
!      Tsfc = Tsfc * 0.002
!      sst  = sst  * 0.001 + 20.0
! hi /= 1000
! hs /= 1000
! Tfsc *= .002f 
! uvel *= 0.001f
! vvel *= 0.001f
! sst *= .001f ; += 20;
      WHERE (aice .EQ. 1e30) aice = 0
      WHERE (hi .EQ. 1e30) hi = 0
      WHERE (hs .EQ. 1e30) hs = 0
      WHERE (sst .EQ. 1e30) sst = 0
      PRINT *,'aice ',MAXVAL(aice), MINVAL(aice)
      PRINT *,'hi   ',MAXVAL(hi  ), MINVAL(hi  )
      PRINT *,'hs   ',MAXVAL(hs  ), MINVAL(hs  )
      PRINT *,'Tsfc ',MAXVAL(Tsfc), MINVAL(Tsfc)
      PRINT *,'tlat ',MAXVAL(tlat), MINVAL(tlat)
      PRINT *,'tlon ',MAXVAL(tlon), MINVAL(tlon)
      PRINT *,'sst  ',MAXVAL(sst ), MINVAL(sst )

      OPEN (10, FILE="binout", FORM="UNFORMATTED", STATUS="UNKNOWN")
      WRITE (10) aice
      WRITE (10) hi
      WRITE (10) hs
      WRITE (10) Tsfc
      WRITE (10) tlat
      WRITE (10) tlon
      WRITE (10) sst
      CLOSE (10)

 
      END
      SUBROUTINE check(status)
      USE netcdf
      IMPLICIT none
      INTEGER, intent(in) :: status
      IF (status /= nf90_noerr) THEN
        PRINT *,nf90_strerror(status)
        STOP "erredout"
      ENDIF
      RETURN
      END
