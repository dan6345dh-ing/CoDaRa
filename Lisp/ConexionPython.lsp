(defun c:ObteneryExportarLineas (/ line nlines i lineactual) 
  (setq PuntoRef (getpoint "\nPuntosdeReferencia"))
  (setq lines (ssget '((0 . "LINE"))))
  (setq nlines (sslength lines))
  (setq txtpuntos (open "C:/USERS/PC-002/DOCUMENTS/CODARA/LISP/txtpoint.txt" "w"))    
  (princ txtpuntos)
  
        
(write-line (strcat (rtos (car PuntoRef)) "," (rtos(cadr PuntoRef)) "," (rtos(caddr PuntoRef))) txtpuntos)
         
  (setq i 0)
  
  (while (< i nlines) 
    (princ i)
    
    (setq lineactual (ssname lines i))
    (princ lineactual)
    (setq i (1+ i))
    (setq Spoint (getpropertyvalue lineactual "StartPoint"))
    (setq Epoint (getpropertyvalue lineactual "EndPoint"))
    (write-line (strcat (rtos (car Spoint)) ","
                        (rtos (cadr Spoint)) ","
                        (rtos (caddr Spoint))
                        ";"
                        (rtos (car Epoint)) ","
                        (rtos (cadr Epoint)) ","
                        (rtos (caddr Epoint))) txtpuntos)
  )
)