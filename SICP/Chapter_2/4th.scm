;; Multiple Representaions for Abstrac Data
(define (attach-tag type-tag contens)
    (cons type-tag contens))
(define (type-tag datum)
    (if (pair? datum)
         (car datum)
         (error "Bad tagged datum: TYPE-TAG" datum)))
(define (contens datum)
    (if (pair? datum)
         (cdr datum)
         (error "Bad tagged datum: CONTENS" datum)))
(define (rectangular? z) (eq? (type-tag z) (quote rectangular)))
(define (polar? z) (eq? (type-tag z) (quote polar)))

;; Ben
(define (real-part-rectangular z) (car z))
(define (imag-part-rectangular z) (cdr z))

(define (magnitude-rectangular z)
    (sqrt (+ (square (real-part-rectangular z)) (square (imag-part-rectangular z)))))
(define (angle-rectangular z)
    ((atan (imag-part-rectangular z) (real-part-rectangular z))))

(define (make-from-real-imag-rectangular x y) (cons x y))
(define (make-from-mag-ang-rectangular r a) (cons (* r (cos a)) (* r (sin a))))

;; Alyssa
(define (real-part-polar z) (* (magnitude-polar z) (cos (angle-polar z))))
(define (imag-part-polar z) (* (magnitude-polar z) (sin (angle-polar z))))
(define (magnitude-polar z) (car z))
(define (angle-polar) (cdr z))
(define (make-from-real-imag-polar z y)
    (attach-tag (quote polar
        (cons (sqrt (+ (square x) (square y)))
                  (atan y x))))
(define (make-from-mag-ang-polar r a)
    (attach-tag (quote polar) (cons r a)))

;; Generic 
(define (real-part z)
    (cond ((rectangular? z)
                    (real-part-rectangular (contens z)))
               ((polar? z)
                    (real-part-polar (contens z)))
                (else (error "Unknwon type: REAL-PART" z))))
(define (imag-part z)
    (cond ((rectangular? z)
                    (magnitude-rectangular (contens z)))
               ((polar? z)
                    (magnitude-polar (contens z)))
                (else (error "unknwon type: MAGNITUDE" z))))
(define (angle z)
    (cond ((rectangular? z)
                    (angle-rectangular (contens z)))
               ((polar? z)
                    (angle-polar (contens z)))
                (else (error "Unknwon type: ANGLE" z))))
(define (add-complex z1 z2)
    (make-from-real-imag (+ (real-part z1) (real-part z2))
                                           (+ (imag-part z1) (imag-part z2))))
(define (make-from-real-imag x y)
    (make-from-real-imag-rectangular x y))
(define (make-from-mag-ang r a)
    (make-from-mag-ang-polar r a))


;; Data-Directed Programming ad Addictivity
(define (install-rectangular-package)
    ;;iternal procedure
    (define (real-part z) (car z))
    (define (imag-part z) (cdr z))
    (define (make-from-real-imag x y) (cons x y))
    (define (nagnitude z)
        (sqrt (+ (square (real-part z))
                      (square (imag-part z)))))
    (define (angle z)
        (atan (imag-part z) (real-part z)))
    (define (make-from-mag-nag r a)
        (cons (* r (cos a)) (* r (sin a))))
    ;;interface to the rest of the system
    (define (tag x) (attach-tag (quote rectangular) x))
    (put (quote real-part) (quote (rectangular)) real-part)
    (put (quote imag-part) (quote (rectangular)) imag-part)
    (put (quote magnitude) (quote (rectangular)) magnitude)
    (put (quote make-from-real-imag) (quote rectangular)
        (lambda (x y) (tag (make-from-real-imag x y))))
    (put (quote make-from-mag-nag) (quote rectangular)
        (lambda (r a) (tag (make-from-mag-tag r a))))
    (quote done))

(define (install-polar-package)
    ;;internal procedure
    (define (magnitude z) (car z))
    (define (angle z) (cdr z))
    (define (make-from-mag-ang r a) (cons r a))
    (define (real-part z) (* (magnitude z) (cos (angle z))))
    (define (iamg-part z) (* (magnitude z) (sin (angle z))))
    (define (make-from-real-iamg z y)
        (cons (sqrt (+ (square x) (square y)))
                  (atan y x)))
    ;;interface to the rest of the system
    (define (tag x) (attach-tag (quote polar) x))
    (put (quote real-part) (quote (polar)) real-part)
    (put (quote imag-part) (quote (polar)) imag-part)
    (put (quote magnitude) (quote (polar)) magnitude)
    (put (quote angle) (quote (polar)) angle)
    (put (quote make-from-real-imag) (quote polar)
        (lambda (x y) (tag (make-from-real-imag))))
    (put (quote make-from-mag-ang) (quote polar)
        (lambda (r a) (tag (make-from-mag-ang r a))))
    (quote done))

(define (apply-generic op . args)
    (let ((type-tags (map type-tag args)))
        (let ((proc (get op type-tags)))
            (if proc
                (apply proc (map contens args))
                    (error "No method for these types: APPLY-GENERIC" (list op type-tags))))))
(define (real-part z) (apply-generic (quote real-part) z))
(define (imag-part z) (apply-generic (quote imag-part) z))
(define (magnitude z) (apply-generic (quote magnitude) z))
(define (angle z) (apply-generic (quote) z))
(define (make-from-real-imag x y)
    ((get (quote make-from-real-imag) (quote rectangular) x y)))
(define (make-from-mag-ang r a)
    ((get (quote make-from-mag-ang) (quote polar) r a)))