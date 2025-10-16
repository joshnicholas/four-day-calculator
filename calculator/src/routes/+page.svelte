<script>
	import BarChart from '$lib/BarChart.svelte';

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
</script>

<div class="mx-auto max-w-[800px] min-h-[700px] text-center px-[5px]" style="padding-top: 20px;">
    <h1 style="margin-top: 40px;">Four day work week calculator</h1>
    <p style="margin-top: 20px;">What's the best day to drop if you're going to a four day week?</p>
        <p style="margin-top: 20px;">Depends on where you live:</p>
	<div style="margin-top: 20px;">
		<select bind:value={selectedRegion} class="border-2 border-black" style="padding: 4px;">
			{#each regions as region}
				<option value={region}>{region}</option>
			{/each}
		</select>
	</div>

	<div style="margin-top: 40px;">
		<h4 style="margin-bottom: 20px;">
			Public holidays by weekday in
			<select bind:value={selectedYear} class="border-2 border-black bg-transparent" style="padding: 4px;">
				{#each years as year}
					<option value={year}>{year}</option>
				{/each}
			</select>
		</h4>
		<BarChart year={selectedYear} region={selectedRegion} />
	</div>

</div>


<div class="footer mx-auto max-w-[800px]">
    <p>This is still under construction.</p>

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