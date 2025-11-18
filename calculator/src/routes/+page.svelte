<script>
	import BarChart from '$lib/BarChart.svelte';
	import SmallMultiplesBarChart from '$lib/SmallMultiplesBarChart.svelte';
	import consecutiveDaysData from '$lib/consecutive_days.json';

	let selectedRegion = $state('Victoria');
	let selectedYear = $state('2026');

	const regions = [
		// 'Australia',
		'New South Wales',
		'Queensland',
		'Tasmania',
		'Victoria',
		'Western Australia',
		'Northern Territory',
		'South Australia',
		'Australian Capital Territory'
	];

	const years = ['2025', '2026', '2027', '2028'];
	const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
</script>


<div class="mx-auto max-w-[800px] min-h-[700px] text-center px-[5px]" style="padding-top: 20px;">

<header>            <h1 style="color:grey">Still under construction. Have not finalised the maths.</h1></header>

	<h1 style="margin-top: 40px;">Four day work week calculator</h1>
    <p style="margin-top: 20px;">What's the best day to drop if you're going to a four day week?</p>
        <p style="margin-top: 20px;">Depends on where you live:</p>
	<div style="margin-top: 20px;">
		<select bind:value={selectedRegion} class="border-2 border-black" style="padding: 4px; border-color: black; border-width: 2px; border-style: solid;">
			{#each regions as region}
				<option value={region}>{region}</option>
			{/each}
		</select>
	</div>

		<div style="margin-top: 20px;">
		<h4 style="margin-bottom: 10px;">How many weekends you get, by day
		</h4>
		    <!-- <p style="margin-bottom: 20px; font-size: .8em">What's the best day to drop if you're going to a four day week?</p> -->
		<SmallMultiplesBarChart
			data={consecutiveDaysData}
			region={selectedRegion}
			weekdays={weekdays}
			years={years}
		/>
	</div>

	<div style="margin-top: 40px;">
		<h4 style="margin-bottom: 20px;">
			Public holidays by weekday in
			<select bind:value={selectedYear} class="border-2 border-black" style="padding: 4px; border-color: black; border-width: 2px; border-style: solid;">
				{#each years as year}
					<option value={year}>{year}</option>
				{/each}
			</select>
		</h4>
		<BarChart year={selectedYear} region={selectedRegion} />
	</div>

	<!-- <div style="margin-top: 40px;">
		<h4 style="margin-bottom: 10px;">Best day to drop for a four day week
		</h4>
		    <p style="margin-bottom: 20px; font-size: .8em">What's the best day to drop if you're going to a four day week?</p>
		<SmallMultiplesBarChart
			data={consecutiveDaysData}
			region={selectedRegion}
			weekdays={weekdays}
			years={years}
		/>
	</div> -->

</div>


<div class="footer mx-auto max-w-[800px]">
    <!-- <p>This is still under construction.</p> -->

    <p>By  <a href="https://joshnicholas.com" target="_blank" rel="noopener noreferrer">Josh</a></p>
</div>


<style>

        .footer {
        text-align: center;
        font-size: 0.75em;
        color: #000;
        margin-top: 40px;
        padding-bottom: 20px;
    }

    .footer p {
        margin: 8px 0;
    }

    .footer a {
        color: #000;
        text-decoration: underline;
    }

    .footer a:hover {
        opacity: 0.7;
    }
</style>