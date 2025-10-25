<script>
	import { scaleLinear, scaleBand } from 'd3-scale';

	let { data, region = 'Victoria', weekdays = [], years = [] } = $props();

	let scaleByWeekday = $state(false);
	let containerWidths = $state({});
	let isMobile = $state(false);

	const chartHeight = 80;
	const margin = { top: 10, right: 5, bottom: 20, left: 5 };

	const weekendTypes = ['Three day weekends', 'Four day weekends', 'Five day weekends'];

	// Check for mobile on mount
	$effect(() => {
		if (typeof window !== 'undefined') {
			const checkMobile = () => {
				isMobile = window.innerWidth < 640;
			};
			checkMobile();
			window.addEventListener('resize', checkMobile);
			return () => window.removeEventListener('resize', checkMobile);
		}
	});

	// Calculate max count for each year across all weekdays
	const yearMaxCounts = $derived.by(() => {
		const maxes = {};
		years.forEach((year) => {
			let max = 0;
			weekdays.forEach((weekday) => {
				const yearData = data?.[region]?.[year]?.[weekday];
				if (yearData) {
					weekendTypes.forEach((type) => {
						const count = yearData[type] || 0;
						if (count > max) max = count;
					});
				}
			});
			maxes[year] = max;
		});
		return maxes;
	});

	// Get chart data for each weekday and year combination
	const chartData = $derived.by(() => {
		return weekdays.map((weekday) => {
			const yearCharts = years.map((year) => {
				const yearData = data?.[region]?.[year]?.[weekday];
				if (!yearData) return { year, values: [] };

				const values = weekendTypes.map((type) => ({
					type: type.replace(' weekends', ''),
					count: yearData[type] || 0
				}));

				return { year, values };
			});

			// Calculate max for this weekday across all years
			let weekdayMax = 0;
			yearCharts.forEach((chart) => {
				chart.values.forEach((v) => {
					if (v.count > weekdayMax) weekdayMax = v.count;
				});
			});

			return { weekday, yearCharts, weekdayMax };
		});
	});

	// Calculate global max for all years scaling
	const globalMax = $derived.by(() => {
		let max = 0;
		chartData.forEach((weekdayData) => {
			if (weekdayData.weekdayMax > max) max = weekdayData.weekdayMax;
		});
		return max;
	});

	// Calculate scales for each chart
	const getScales = (values, containerWidth, weekdayMax) => {
		const innerWidth = containerWidth - margin.left - margin.right;
		const innerHeight = chartHeight - margin.top - margin.bottom;

		let maxCount;
		if (scaleByWeekday) {
			// Use max for this weekday row
			maxCount = weekdayMax;
		} else {
			// Use global max across entire dataset
			maxCount = globalMax;
		}

		// Always use full domain for consistent positioning
		const allTypes = weekendTypes.map((type) => type.replace(' weekends', ''));
		const xScale = scaleBand()
			.domain(allTypes)
			.range([0, innerWidth])
			.padding(0.5);

		const yScale = scaleLinear().domain([0, maxCount]).range([innerHeight, 0]);

		return { xScale, yScale, innerWidth, innerHeight };
	};
</script>

<div style="width: 100%;">
	<div style="margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; justify-content: center;">
		<button
			onclick={() => (scaleByWeekday = !scaleByWeekday)}
			class="border-2 border-black"
			style="padding: 4px 8px; cursor: pointer; background: transparent;"
		>
			Scale by: {scaleByWeekday ? 'Weekday' : 'All data'}
		</button>
	</div>

	{#each chartData as weekdayData, weekdayIndex}
		<div style="margin-bottom: 0px; display: flex; align-items: center;">
			<!-- Rotated weekday label on the left -->
			<div style="width: 40px; display: flex; justify-content: center; align-items: center;">
				<span style="writing-mode: vertical-rl; transform: rotate(180deg); font-weight: bold; font-size: 12px;">
					{weekdayData.weekday}
				</span>
			</div>

			<div style="flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 3px;">
				{#each weekdayData.yearCharts as chart}
					{@const chartKey = `${weekdayData.weekday}-${chart.year}`}
					<div style="width: 100%;" bind:clientWidth={containerWidths[chartKey]}>
						<!-- Only show year on first row -->
						{#if weekdayIndex === 0}
							<h6 style="margin: 0 0 2px 0; font-weight: bold; font-size: 11px; text-align: center;">{chart.year}</h6>
						{:else}
							<div style="height: 13px;"></div>
						{/if}
						{#if containerWidths[chartKey]}
							{@const { xScale, yScale, innerWidth, innerHeight } = getScales(
								chart.values,
								containerWidths[chartKey],
								weekdayData.weekdayMax
							)}
							<svg width="100%" height={chartHeight} style="max-width: 100%;">
								<g transform="translate({margin.left}, {margin.top})">
									<!-- Bars -->
									{#each chart.values as item}
										{@const isMax = item.count === yearMaxCounts[chart.year] && item.count > 0}
										<rect
											x={xScale(item.type)}
											y={yScale(item.count)}
											width={xScale.bandwidth()}
											height={innerHeight - yScale(item.count)}
											fill={isMax ? '#fa9a7a' : 'transparent'}
											stroke="black"
											stroke-width="1"
										/>

										<!-- Value labels -->
										{#if item.count > 0}
											<text
												x={xScale(item.type) + xScale.bandwidth() / 2}
												y={yScale(item.count) - 2}
												text-anchor="middle"
												fill="black"
												font-size="8"
											>
												{item.count}
											</text>
										{/if}
									{/each}

									<!-- X-axis labels - only on first and last weekday -->
									{#if weekdayIndex === 0 || weekdayIndex === chartData.length - 1}
										{#each chart.values as item}
											<text
												x={xScale(item.type) + xScale.bandwidth() / 2}
												y={innerHeight + 10}
												text-anchor="middle"
												fill="black"
												font-size={isMobile ? '7' : '8'}
											>
												{item.type.split(' ')[0]}
											</text>
											<text
												x={xScale(item.type) + xScale.bandwidth() / 2}
												y={innerHeight + 18}
												text-anchor="middle"
												fill="black"
												font-size={isMobile ? '7' : '8'}
											>
												day
											</text>
										{/each}
									{/if}
								</g>
							</svg>
						{/if}
					</div>
				{/each}
			</div>
		</div>
	{/each}
</div>
