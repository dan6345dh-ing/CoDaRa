(defun c:MoveRectsToPoints ( / ss n i ent obj minPt maxPt basePt ptList dstPt)
  (princ "\nSelecciona los rectangulos: ")
  (setq ss (ssget '((0 . "LWPOLYLINE")))) ;; selecciona polilineas (rectángulos)
  (if ss
    (progn
      ;; lista de puntos destino (puedes cambiar o pedirlos al usuario)
      (setq ptList '(
                      	(0 0 0)
			(0 100 0)
			(0 200 0)
			(0 300 0)
			(0 400 0)
			(0 500 0)
			(0 600 0)
			(0 700 0)
			(0 800 0)
                    ))


      (setq n 0)
      (setq i 0)

      (while (< i (sslength ss))
        (setq ent (ssname ss i))
        (setq obj (vlax-ename->vla-object ent))

        ;; obtener bounding box del rectángulo
        (vla-getboundingbox obj 'minPt 'maxPt)
        (setq minPt (vlax-safearray->list minPt))
        (setq maxPt (vlax-safearray->list maxPt))

        ;; esquina inferior izquierda = (x_min, y_min)
        (setq basePt (list (car minPt) (cadr minPt) 0.0))

        ;; obtener punto destino (si existe en la lista)
        (if (< n (length ptList))
          (progn
            (setq dstPt (nth n ptList))
            ;; mover
            (command "_.MOVE" ent "" basePt dstPt)
            (setq n (1+ n))
          )
        )
        (setq i (1+ i))
      )
    )
    (princ "\nNo se seleccionaron rectángulos.")
  )
  (princ)
)

(defun c:MoveRectGroups ( / ssRects ptList n rectObj minPt maxPt basePt ssInside allSet dstPt)

  ;; Lista de puntos destino (edítala como quieras o haz que se pidan al usuario)
  (setq ptList '(
                      	(0 0 0)
			(0 100 0)
			(0 200 0)
			(0 300 0)
			(0 400 0)
			(0 500 0)
			(0 600 0)
			(0 700 0)
			(0 800 0)
                ))

  (princ "\nSelecciona los rectángulos contenedores: ")
  (setq ssRects (ssget '((0 . "LWPOLYLINE")))) ;; solo polilíneas rectangulares
  (setq n 0)

  (if ssRects
    (while (< n (length ptList))
      (setq rectObj (ssname ssRects n))

      ;; obtener bounding box del rectángulo
      (vla-getboundingbox (vlax-ename->vla-object rectObj) 'pmin 'pmax)
      (setq minPt (vlax-safearray->list pmin))
      (setq maxPt (vlax-safearray->list pmax))

      ;; esquina inferior izquierda
      (setq basePt (list (car minPt) (cadr minPt) 0.0))

      ;; objetos dentro del rectángulo
      (setq ssInside (ssget "C" minPt maxPt)) 

      ;; crear conjunto combinado: rectángulo + objetos dentro
      (setq allSet (ssadd rectObj))
      (if ssInside
        (repeat (sslength ssInside)
          (setq allSet (ssadd (ssname ssInside 0) allSet))
          (ssdel (ssname ssInside 0) ssInside)
        )
      )

      ;; destino
      (setq dstPt (nth n ptList))

      ;; mover todo el conjunto
      (command "_.MOVE" allSet "" basePt dstPt)

      (setq n (1+ n))
    )
  )
  (princ)
)
