
function abrir1()
{
	const v = document.querySelector('#tooltip');
	const icono = document.querySelector('#montoprestamo');

	const x = icono.offsetRigth;
	const y = icono.offsetTop;

		// Calculamos el tamaño del tooltip.
	const anchoTooltip = v.clientWidth;
	const altoTooltip = v.clientHeight;

		// Calculamos donde posicionaremos el tooltip.
	const izquierda = x - (anchoTooltip / 2) + 15;
	const arriba = y - altoTooltip + 10;

	v.style.left = `${izquierda}px`;
	v.style.top = `${arriba}px`;
	v.classList.add('activo');
}

function cerrar1()
{
	const v = document.querySelector('#tooltip');
	v.classList.remove('activo');
}

function abrir2()
{
	const v1 = document.querySelector('#tooltip1');
	const icono1 = document.querySelector('#montoadelanto');

	const x1 = icono1.offsetRigth;
	const y1 = icono1.offsetTop;

		// Calculamos el tamaño del tooltip.
	const anchoTooltip1 = v1.clientWidth;
	const altoTooltip1 = v1.clientHeight;

		// Calculamos donde posicionaremos el tooltip.
	const izquierda1 = x1 - (anchoTooltip1 / 2) + 15;
	const arriba1 = y1 - altoTooltip1 + 10;

	v1.style.left = `${izquierda1}px`;
	v1.style.top = `${arriba1}px`;

	v1.classList.add('activo');
}

function cerrar2()
{
	const v = document.querySelector('#tooltip1');
	v.classList.remove('activo');
}

function abrir3()
{
	const v2 = document.querySelector('#tooltip2');
	const icono2 = document.querySelector('#cuotas');

	const x2 = icono2.offsetRigth;
	const y2 = icono2.offsetTop;

		// Calculamos el tamaño del tooltip.
	const anchoTooltip2 = v2.clientWidth;
	const altoTooltip2 = v2.clientHeight;

		// Calculamos donde posicionaremos el tooltip.
	const izquierda2 = x2 - (anchoTooltip2 / 2) + 15;
	const arriba2 = y2 - altoTooltip2 + 10;

	v2.style.left = `${izquierda2}px`;
	v2.style.top = `${arriba2}px`;

	v2.classList.add('activo');
}

function cerrar3()
{
	const v = document.querySelector('#tooltip2');
	v.classList.remove('activo');
}

function abrir4()
{
	const v3 = document.querySelector('#tooltip3');
	const icono3 = document.querySelector('#pagar');

	const x3 = icono3.offsetRigth;
	const y3 = icono3.offsetTop;

		// Calculamos el tamaño del tooltip.
	const anchoTooltip3 = v3.clientWidth;
	const altoTooltip3 = v3.clientHeight;

		// Calculamos donde posicionaremos el tooltip.
	const izquierda3 = x3 - (anchoTooltip3 / 1) - 65;
	const arriba3 = y3 - altoTooltip3 + 10;

	v3.style.left = `${izquierda3}px`;
	v3.style.top = `${arriba3}px`;

	v3.classList.add('activo');
}

function cerrar4()
{
	const v3 = document.querySelector('#tooltip3');
	v3.classList.remove('activo');
}