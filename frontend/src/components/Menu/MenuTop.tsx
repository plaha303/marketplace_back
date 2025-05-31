import classNames from 'classnames';
import styles from './Menu.module.scss';



const currencies = [
	{ id: '1', name: '₴' },
	{ id: '2', name: '$' },
	{ id: '3', name: '€' },
];

const languages = [
	{ id: '1', name: 'ua' },
	{ id: '2', name: 'us' },
];

function MenuTop() {
	return (
		<div className={classNames(styles['menuTop container'])}>

		</div>
	);
}

export default MenuTop;
