(defun c:InterMulti ( / ss n i j e1 e2 obj1 obj2 p1 p2 p3 p4 inter)
  (princ "\nSelecciona las líneas para calcular intersecciones: ")
  (setq ss (ssget '((0 . "LINE")))) ; solo acepta objetos tipo LINE
  (setvar "OSMODE" 0)
  (if ss
    (progn
      (setq n (sslength ss)) ; número de líneas
      (setq i 0)
      ;; recorrer todas las combinaciones de líneas
      (while (< i n)
        (setq e1 (ssname ss i)
              obj1 (vlax-ename->vla-object e1)
              p1 (vlax-get obj1 'StartPoint)
              p2 (vlax-get obj1 'EndPoint))
        (setq j (1+ i))
        (while (< j n)
          (setq e2 (ssname ss j)
                obj2 (vlax-ename->vla-object e2)
                p3 (vlax-get obj2 'StartPoint)
                p4 (vlax-get obj2 'EndPoint))

          ;; calcular intersección (nil = solo segmentos reales, T = líneas infinitas)
          (setq inter (inters p1 p2 p3 p4 T))

          (if inter
            (progn
              (command "._POINT" inter)
            )
          )
          (setq j (1+ j))
        )
        (setq i (1+ i))
      )
      (princ "\nProceso terminado.")
    )
    (princ "\nNo seleccionaste ninguna línea.")
  )
  (princ)

)

(defun c:LinFinIni ( / ss n i j e1 e2 obj1 obj2 p1 p2 p3 p4 inter)
  (princ "\nSelecciona las líneas: ")
  (setq ss (ssget '((0 . "LINE")))) ; solo acepta objetos tipo LINE
  (setvar "OSMODE" 0)
  (if ss
    (progn
      (setq n (sslength ss)) ; número de líneas
      (setq i 0)
      ;; recorrer todas las combinaciones de líneas
      (while (< i n)
        (setq e1 (ssname ss i)
              obj1 (vlax-ename->vla-object e1)
              p1 (vlax-get obj1 'StartPoint)
              p2 (vlax-get obj1 'EndPoint))
        (progn
              (command "._POINT" p1)
              (command "._POINT" p2)
        )
        (setq i (1+ i))
      )
    )
  )
)