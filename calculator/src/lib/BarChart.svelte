<script>
	import { scaleLinear, scaleBand } from 'd3-scale';
	import stateCountsData from './state_counts.json';

	let { year = '2026', region = 'Victoria' } = $props();

	let containerWidth = $state(600);
	const height = 400;
	const margin = { top: 20, right: 30, bottom: 40, left: 100 };

	const width = $derived(containerWidth);
	const innerWidth = $derived(width - margin.left - margin.right);
	const innerHeight = height - margin.top - margin.bottom;


	const weekdayOrder = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];


	const data = $derived.by(() => {
		const rawData = stateCountsData[year]?.[region];
		if (!rawData) return [];
		return JSON.parse(rawData);
	});

	// Create scales
	const xScale = $derived(
		scaleLinear()
			.domain([0, Math.max(...data.map((d) => d.Count), 0)])
			.range([0, innerWidth])
	);

	const yScale = $derived(
		scaleBand()
			.domain(weekdayOrder)
			.range([0, innerHeight])
			.padding(0.2)
	);


	const orderedData = $derived(
		weekdayOrder.map(day => data.find(d => d.Weekday === day))
	);
</script>

<div bind:clientWidth={containerWidth} style="width: 100%; max-width: 600px; margin: 0 auto;">
<svg {width} {height} style="max-width: 100%; height: auto;">
	<g transform="translate({margin.left}, {margin.top})">

		{#each weekdayOrder as day}
			<text
				x={-10}
				y={yScale(day) + yScale.bandwidth() / 2}
				text-anchor="end"
				dominant-baseline="middle"
				fill="black"
				font-size="14"
			>
				{day}
			</text>
		{/each}


		{#each orderedData as item}
			{#if item}
				<rect
					x={0}
					y={yScale(item.Weekday)}
					width={xScale(item.Count)}
					height={yScale.bandwidth()}
					fill="transparent"
					stroke="black"
					stroke-width="2"
				/>

				<text
					x={xScale(item.Count) + 5}
					y={yScale(item.Weekday) + yScale.bandwidth() / 2}
					dominant-baseline="middle"
					fill="black"
					font-size="14"
				>
					{item.Count}
				</text>
			{/if}
		{/each}
	</g>
</svg>
</div>
